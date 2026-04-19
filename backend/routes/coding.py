from flask import Blueprint, request, jsonify, session
from functools import wraps
import subprocess
import tempfile
import os
import time
import uuid
from datetime import datetime
import docker
import psutil
from pymongo import MongoClient
from activity_logger import log_user_activity, resolve_user_identity
from services.real_compiler_service import real_compiler_service

bp = Blueprint('coding', __name__)

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client.openlearnx

def secure_execution_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is in secure coding mode
        if not session.get('secure_coding_mode'):
            return jsonify({"error": "Secure coding mode required"}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/start-session", methods=["POST"])
def start_coding_session():
    """Start a secure coding session"""
    try:
        data = request.json
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')
        
        session_id = str(uuid.uuid4())
        session['coding_session_id'] = session_id
        session['secure_coding_mode'] = True
        session['start_time'] = datetime.now().isoformat()
        session['course_id'] = course_id
        session['lesson_id'] = lesson_id

        identity = resolve_user_identity(request, db)
        log_user_activity(
            db,
            identity.get("user_id"),
            "coding",
            "Started coding session",
            "Entered secure coding session",
            {
                "session_id": session_id,
                "course_id": course_id,
                "lesson_id": lesson_id,
            },
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Secure coding session started",
            "restrictions": {
                "copy_paste_disabled": True,
                "browser_locked": True,
                "extensions_blocked": True,
                "virtual_detection": True
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/execute", methods=["POST"])
@secure_execution_required
def execute_code():
    """Execute code securely in isolated environment"""
    try:
        data = request.json
        code = data.get('code')
        language = data.get('language', 'python')
        test_cases = data.get('test_cases', [])
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Log coding attempt
        log_coding_attempt(session['coding_session_id'], code, language)
        
        # Execute code in hardened Docker sandbox
        result = real_compiler_service.execute_code(code=code, language=language, input_data="")

        event_type = "coding_execution_success" if result.get("success") else "coding_execution_blocked"
        severity = "info" if result.get("success") else "warning"

        execution_status = "success" if result.get("success") else "failed"
        if result.get("blocked"):
            execution_status = "blocked"

        db.security_logs.insert_one({
            "timestamp": datetime.utcnow(),
            "event_type": event_type,
            "action": "secure_coding_execute",
            "status_code": 200 if result.get("success") else 400,
            "severity": severity,
            "path": request.path,
            "method": request.method,
            "ip": request.remote_addr or "unknown",
            "user_agent": request.headers.get("User-Agent", ""),
            "metadata": {
                "language": language,
                "execution_id": result.get("execution_id"),
                "blocked": bool(result.get("blocked")),
                "security_violations": result.get("security_violations", []),
                "execution_time": result.get("execution_time", 0),
                "memory_used": result.get("memory_used", 0),
                "exit_code": result.get("exit_code", -1),
            },
            "metadata_text": str(result.get("security_violations", [])),
        })

        try:
            request_payload = {
                "language": language,
                "code": (code or "")[:4000],
                "code_size": len(code or ""),
                "test_case_count": len(test_cases) if isinstance(test_cases, list) else 0,
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
                "exit_code": result.get("exit_code", -1),
            }

            db.code_execution_events.insert_one({
                "timestamp": datetime.utcnow(),
                "event_type": "execution",
                "source": "coding",
                "language": language,
                "execution_id": result.get("execution_id"),
                "execution_time": result.get("execution_time", 0),
                "memory_used": result.get("memory_used", 0),
                "exit_code": result.get("exit_code", -1),
                "status": execution_status,
                "blocked": bool(result.get("blocked")),
                "security_violations": result.get("security_violations", []),
                "error": result.get("error", ""),
                "request_body": request_payload,
                "response_body": response_payload,
                "ip": request.remote_addr or "unknown",
                "user_agent": request.headers.get("User-Agent", ""),
            })
        except Exception:
            pass

        if result.get("success"):
            return jsonify({"success": True, **result})
        return jsonify({"success": False, **result}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/submit-test", methods=["POST"])
@secure_execution_required
def submit_coding_test():
    """Submit coding test for evaluation"""
    try:
        data = request.json
        code = data.get('code')
        problem_id = data.get('problem_id')
        
        # Validate against test cases
        test_result = validate_test_submission(code, problem_id)
        
        # Store submission
        submission_id = store_submission(
            session['coding_session_id'],
            session['course_id'],
            problem_id,
            code,
            test_result
        )

        identity = resolve_user_identity(request, db)
        resolved_user_id = identity.get("user_id")
        if resolved_user_id:
            db.user_submissions.insert_one({
                "user_id": resolved_user_id,
                "session_id": session.get('coding_session_id'),
                "course_id": session.get('course_id'),
                "problem_id": problem_id,
                "score": test_result.get('score', 0),
                "points_earned": int(test_result.get('score', 0)),
                "submitted_at": datetime.now(),
                "status": "submitted",
            })

            log_user_activity(
                db,
                resolved_user_id,
                "coding",
                "Submitted coding solution",
                f"Submitted coding test for problem '{problem_id}'",
                {
                    "submission_id": submission_id,
                    "problem_id": problem_id,
                    "score": test_result.get('score', 0),
                    "passed": test_result.get('passed', 0),
                    "total": test_result.get('total', 0),
                },
                points_earned=int(test_result.get('score', 0)),
            )
        
        return jsonify({
            "success": True,
            "submission_id": submission_id,
            "score": test_result['score'],
            "passed_tests": test_result['passed'],
            "total_tests": test_result['total'],
            "feedback": test_result['feedback']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def execute_in_container(code, language, test_cases):
    """Backward-compatible wrapper around the hardened compiler service."""
    result = real_compiler_service.execute_code(code=code, language=language, input_data="")
    if result.get("success"):
        return {
            "success": True,
            "output": result.get("output", ""),
            "test_results": [],
            "execution_time": result.get("execution_time", 0),
            "memory_used": result.get("memory_used", 0),
            "execution_id": result.get("execution_id"),
        }
    return {
        "success": False,
        "error": result.get("error", "Execution failed"),
        "security_violations": result.get("security_violations", []),
        "execution_id": result.get("execution_id"),
    }

def get_file_extension(language):
    extensions = {
        'python': 'py',
        'java': 'java',
        'javascript': 'js'
    }
    return extensions.get(language, 'txt')

def get_run_command(language, filename):
    commands = {
        'python': f'python /app/{os.path.basename(filename)}',
        'java': f'javac /app/{os.path.basename(filename)} && java -cp /app {os.path.splitext(os.path.basename(filename))[0]}',
        'javascript': f'node /app/{os.path.basename(filename)}'
    }
    return commands.get(language)

def log_coding_attempt(session_id, code, language):
    """Log all coding attempts for monitoring"""
    db.coding_logs.insert_one({
        "session_id": session_id,
        "code": code,
        "language": language,
        "timestamp": datetime.now(),
        "ip_address": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    })

def validate_test_submission(code, problem_id):
    """Validate code against predefined test cases"""
    # Load test cases for the problem
    test_cases = get_problem_test_cases(problem_id)
    
    passed = 0
    total = len(test_cases)
    feedback = []
    
    for i, test_case in enumerate(test_cases):
        result = run_test_case(code, 'python', test_case)
        if result['passed']:
            passed += 1
            feedback.append(f"Test {i+1}: ✅ Passed")
        else:
            feedback.append(f"Test {i+1}: ❌ Failed - {result['error']}")
    
    score = (passed / total) * 100
    
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "feedback": feedback
    }

def get_problem_test_cases(problem_id):
    """Get test cases for a specific problem"""
    # This would load from your database
    test_cases_db = {
        "python-basics-1": [
            {"input": "hello", "expected_output": "HELLO"},
            {"input": "world", "expected_output": "WORLD"}
        ],
        "java-oop-1": [
            {"input": "5", "expected_output": "25"},
            {"input": "10", "expected_output": "100"}
        ]
    }
    return test_cases_db.get(problem_id, [])
