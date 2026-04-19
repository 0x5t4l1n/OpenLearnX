from datetime import datetime
import os

from flask import Blueprint, jsonify, request
from pymongo import MongoClient

from services.real_compiler_service import real_compiler_service

bp = Blueprint("compiler", __name__)

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.openlearnx


def _json_response(payload, status=200):
    response = jsonify(payload)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response, status


def _client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _log_security(event_type, action, severity="info", status_code=200, metadata=None):
    try:
        log_doc = {
            "timestamp": datetime.utcnow(),
            "event_type": event_type,
            "action": action,
            "status_code": int(status_code),
            "severity": severity,
            "path": request.path,
            "method": request.method,
            "ip": _client_ip(),
            "user_agent": request.headers.get("User-Agent", ""),
            "metadata": metadata or {},
            "metadata_text": str(metadata or {}),
        }
        db.security_logs.insert_one(log_doc)
    except Exception as e:
        print(f"Compiler security log failure: {e}")


@bp.route("/execute", methods=["POST", "OPTIONS"])
def execute_code():
    if request.method == "OPTIONS":
        return _json_response({"status": "ok"}, 200)

    try:
        data = request.get_json(silent=True) or {}
        language = str(data.get("language", "python")).strip().lower()
        code = str(data.get("code", ""))
        input_data = str(data.get("input", ""))

        if not code.strip():
            _log_security(
                "compiler_input_invalid",
                "empty_code_submission",
                severity="warning",
                status_code=400,
                metadata={"language": language},
            )
            return _json_response({"success": False, "error": "No code provided"}, 400)

        result = real_compiler_service.execute_code(code=code, language=language, input_data=input_data)

        log_metadata = {
            "language": language,
            "code_size": len(code),
            "execution_id": result.get("execution_id"),
            "exit_code": result.get("exit_code"),
            "execution_time": result.get("execution_time", 0),
            "memory_used": result.get("memory_used", 0),
            "blocked": bool(result.get("blocked")),
            "security_violations": result.get("security_violations", []),
            "error": result.get("error", ""),
        }

        try:
            status = "success"
            if result.get("blocked"):
                status = "blocked"
            elif result.get("error") and not result.get("success", False):
                status = "failed"

            request_payload = {
                "language": language,
                "code": code[:4000],
                "code_size": len(code),
                "input": input_data[:2000],
                "input_size": len(input_data),
            }
            response_payload = {
                "success": bool(result.get("success")),
                "blocked": bool(result.get("blocked")),
                "execution_id": result.get("execution_id"),
                "output": (result.get("output") or "")[:4000],
                "error": result.get("error", ""),
                "security_violations": result.get("security_violations", []),
                "execution_time": result.get("execution_time", 0),
                "memory_used": result.get("memory_used", 0),
                "exit_code": result.get("exit_code", 0),
            }

            db.code_execution_events.insert_one(
                {
                    "timestamp": datetime.utcnow(),
                    "event_type": "execution",
                    "source": "compiler",
                    "language": language,
                    "execution_id": result.get("execution_id"),
                    "execution_time": result.get("execution_time", 0),
                    "memory_used": result.get("memory_used", 0),
                    "exit_code": result.get("exit_code", 0),
                    "status": status,
                    "blocked": bool(result.get("blocked")),
                    "security_violations": result.get("security_violations", []),
                    "error": result.get("error", ""),
                    "request_body": request_payload,
                    "response_body": response_payload,
                    "ip": _client_ip(),
                    "user_agent": request.headers.get("User-Agent", ""),
                }
            )
        except Exception:
            pass

        if result.get("blocked"):
            _log_security(
                "compiler_security_block",
                "static_policy_blocked_submission",
                severity="warning",
                status_code=400,
                metadata=log_metadata,
            )
            return _json_response({"success": False, **result}, 400)

        if result.get("error") and not result.get("success", False):
            _log_security(
                "compiler_execution_failed",
                "secure_container_execution_failed",
                severity="warning",
                status_code=400,
                metadata=log_metadata,
            )
            return _json_response({"success": False, **result}, 400)

        _log_security(
            "compiler_execution_success",
            "secure_container_execution_completed",
            severity="info",
            status_code=200,
            metadata=log_metadata,
        )

        return _json_response(result, 200)

    except Exception as e:
        _log_security(
            "compiler_internal_error",
            "compiler_route_exception",
            severity="error",
            status_code=500,
            metadata={"error": str(e)},
        )
        return _json_response({"success": False, "error": f"Server error: {str(e)}"}, 500)


@bp.route("/languages", methods=["GET", "OPTIONS"])
def get_supported_languages():
    if request.method == "OPTIONS":
        return _json_response({"status": "ok"}, 200)

    try:
        return _json_response({"success": True, "languages": real_compiler_service.get_supported_languages()}, 200)
    except Exception as e:
        return _json_response({"success": False, "error": str(e)}, 500)


@bp.route("/test", methods=["POST", "OPTIONS"])
def compiler_test():
    if request.method == "OPTIONS":
        return _json_response({"status": "ok"}, 200)

    data = request.get_json(silent=True) or {}
    language = str(data.get("language", "python")).strip().lower()

    smoke_code = {
        "python": 'print("ok")',
        "javascript": 'console.log("ok")',
        "java": "public class Main { public static void main(String[] args){ System.out.println(\"ok\"); } }",
        "c": "#include <stdio.h>\nint main(){ printf(\"ok\\n\"); return 0; }",
        "cpp": "#include <iostream>\nint main(){ std::cout << \"ok\\n\"; return 0; }",
        "go": "package main\nimport \"fmt\"\nfunc main(){ fmt.Println(\"ok\") }",
        "rust": "fn main(){ println!(\"ok\"); }",
    }

    if language not in smoke_code:
        return _json_response({"success": False, "error": f"Unsupported language: {language}"}, 400)

    result = real_compiler_service.execute_code(smoke_code[language], language, "")
    if result.get("success"):
        return _json_response(result, 200)
    return _json_response({"success": False, **result}, 400)


@bp.route("/health", methods=["GET"])
def compiler_health():
    docker_ok = real_compiler_service._get_docker_client() is not None and real_compiler_service.docker_available
    return _json_response(
        {
            "status": "healthy" if docker_ok else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "docker_available": docker_ok,
            "secure_execution_only": True,
            "supported_languages": [l["id"] for l in real_compiler_service.get_supported_languages()],
        },
        200 if docker_ok else 503,
    )
