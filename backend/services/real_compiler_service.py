import ast
import os
import queue
import re
import tempfile
import threading
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import docker


class RealCompilerService:
    def __init__(self):
        self.client = None
        self.execution_queue = queue.Queue()
        self.active_executions: Dict[str, Dict[str, Any]] = {}
        self.max_code_size = 20000
        self.docker_available = False

        # Docker is mandatory for secure execution.
        self.language_configs = {
            "python": {
                "image": "python:3.11-alpine",
                "file_name": "code.py",
                "compile_command": None,
                "run_command": "python /workspace/code.py",
                "timeout": 8,
                "memory_limit": "128m",
                "cpu_limit": 0.35,
            },
            "javascript": {
                "image": "node:20-alpine",
                "file_name": "code.js",
                "compile_command": None,
                "run_command": "node /workspace/code.js",
                "timeout": 8,
                "memory_limit": "128m",
                "cpu_limit": 0.35,
            },
            "c": {
                "image": "gcc:13",
                "file_name": "code.c",
                "compile_command": "gcc -O2 -o /workspace/program /workspace/code.c",
                "run_command": "/workspace/program",
                "timeout": 10,
                "memory_limit": "192m",
                "cpu_limit": 0.5,
            },
            "cpp": {
                "image": "gcc:13",
                "file_name": "code.cpp",
                "compile_command": "g++ -O2 -std=c++17 -o /workspace/program /workspace/code.cpp",
                "run_command": "/workspace/program",
                "timeout": 10,
                "memory_limit": "256m",
                "cpu_limit": 0.5,
            },
            "java": {
                "image": "openjdk:17-alpine",
                "file_name": "Main.java",
                "compile_command": "javac /workspace/Main.java",
                "run_command": "java -cp /workspace Main",
                "timeout": 12,
                "memory_limit": "256m",
                "cpu_limit": 0.5,
            },
            "go": {
                "image": "golang:1.22-alpine",
                "file_name": "code.go",
                "compile_command": "go build -o /workspace/program /workspace/code.go",
                "run_command": "/workspace/program",
                "timeout": 14,
                "memory_limit": "256m",
                "cpu_limit": 0.6,
            },
            "rust": {
                "image": "rust:1.77-alpine",
                "file_name": "code.rs",
                "compile_command": "rustc /workspace/code.rs -o /workspace/program",
                "run_command": "/workspace/program",
                "timeout": 20,
                "memory_limit": "512m",
                "cpu_limit": 0.8,
            },
        }

        self.blocked_python_modules = {
            "os",
            "socket",
            "subprocess",
            "pty",
            "multiprocessing",
            "ctypes",
            "resource",
            "pwd",
            "grp",
            "signal",
            "fcntl",
            "selectors",
            "pathlib",
            "shutil",
        }
        self.blocked_python_calls = {
            "eval",
            "exec",
            "compile",
            "__import__",
            "open",
            "input",
            "globals",
            "locals",
            "vars",
            "getattr",
            "setattr",
            "delattr",
        }
        self.blocked_python_attrs = {
            "fork",
            "forkpty",
            "spawn",
            "spawnl",
            "spawnlp",
            "spawnv",
            "spawnvp",
            "system",
            "popen",
            "execl",
            "execle",
            "execlp",
            "execv",
            "execve",
            "execvp",
            "setsid",
            "dup2",
        }
        self.blocked_patterns = {
            "javascript": [
                r"require\s*\(\s*['\"]child_process['\"]\s*\)",
                r"require\s*\(\s*['\"]net['\"]\s*\)",
                r"require\s*\(\s*['\"]dgram['\"]\s*\)",
                r"process\.env",
                r"process\.binding",
                r"fs\.readFile|fs\.writeFile|fs\.open|fs\.create",
            ],
            "java": [
                r"Runtime\.getRuntime\s*\(",
                r"ProcessBuilder\s*\(",
                r"java\.net\.",
                r"java\.nio\.file\.",
                r"System\.getenv\s*\(",
            ],
            "c": [
                r"\bsystem\s*\(",
                r"\bpopen\s*\(",
                r"\bfork\s*\(",
                r"\bexec[a-z]*\s*\(",
                r"\bsocket\s*\(",
            ],
            "cpp": [
                r"\bsystem\s*\(",
                r"\bpopen\s*\(",
                r"\bfork\s*\(",
                r"\bexec[a-z]*\s*\(",
                r"\bsocket\s*\(",
            ],
            "go": [
                r"\bexec\.Command\s*\(",
                r"\bnet\.",
                r"\bos\.StartProcess\s*\(",
                r"\bos\.Exec\s*\(",
            ],
            "rust": [
                r"std::process::Command",
                r"std::net::",
                r"unsafe\s*\{",
            ],
        }

        self.start_execution_worker()

    def _get_docker_client(self):
        if self.client is None:
            try:
                self.client = docker.from_env()
                self.client.ping()
                self.docker_available = True
            except Exception:
                self.docker_available = False
                self.client = None
        return self.client

    def start_execution_worker(self):
        def worker():
            while True:
                try:
                    execution_task = self.execution_queue.get(timeout=1)
                    self._execute_task(execution_task)
                    self.execution_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Execution worker error: {e}")

        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()

    def _execute_task(self, _execution_task):
        # Queue worker placeholder kept for backward compatibility.
        return None

    def execute_code(self, code: str, language: str, input_data: str = "", execution_id: str = None) -> Dict[str, Any]:
        language = (language or "").lower().strip()
        if language == "js":
            language = "javascript"
        if language == "c++":
            language = "cpp"

        if language not in self.language_configs:
            return {"error": f"Language '{language}' not supported"}

        if not execution_id:
            execution_id = str(uuid.uuid4())

        if not code or not code.strip():
            return {"error": "No code provided", "execution_id": execution_id, "language": language}

        if len(code) > self.max_code_size:
            return {
                "error": f"Code too large. Maximum size is {self.max_code_size} characters.",
                "execution_id": execution_id,
                "language": language,
                "blocked": True,
            }

        ok, violations = self._validate_code_static(code, language)
        if not ok:
            return {
                "error": "Code rejected by security policy",
                "execution_id": execution_id,
                "language": language,
                "blocked": True,
                "security_violations": violations,
            }

        config = self.language_configs[language]
        execution_context = {
            "execution_id": execution_id,
            "code": code,
            "language": language,
            "input_data": input_data or "",
            "config": config,
            "start_time": datetime.utcnow(),
            "status": "running",
        }

        try:
            self.active_executions[execution_id] = execution_context
            result = self._execute_in_container(execution_context)
            execution_context["status"] = "completed"
            execution_context["end_time"] = datetime.utcnow()
            execution_context["result"] = result

            if result.get("error"):
                return {
                    "success": False,
                    "execution_id": execution_id,
                    "output": result.get("output", ""),
                    "error": result.get("error", ""),
                    "execution_time": result.get("execution_time", 0),
                    "memory_used": result.get("memory_used", 0),
                    "exit_code": result.get("exit_code", -1),
                    "language": language,
                    "timestamp": datetime.utcnow().isoformat(),
                }

            return {
                "success": True,
                "execution_id": execution_id,
                "output": result.get("output", ""),
                "error": "",
                "execution_time": result.get("execution_time", 0),
                "memory_used": result.get("memory_used", 0),
                "exit_code": result.get("exit_code", 0),
                "language": language,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "error": f"Execution failed: {str(e)}",
                "execution_id": execution_id,
                "language": language,
            }
        finally:
            self.active_executions.pop(execution_id, None)

    def _validate_code_static(self, code: str, language: str) -> Tuple[bool, List[str]]:
        violations: List[str] = []

        # Generic payload patterns often used for sandbox escape and exfiltration.
        generic_patterns = [
            r"/bin/sh",
            r"/bin/bash",
            r"nc\s+-l|nc\s+-e",
            r"reverse\s*shell",
            r"bash\s+-i",
            r"wget\s+http|curl\s+http",
        ]
        for pattern in generic_patterns:
            if re.search(pattern, code, flags=re.IGNORECASE):
                violations.append(f"Blocked high-risk pattern: {pattern}")

        if language == "python":
            try:
                tree = ast.parse(code)
            except SyntaxError as e:
                return False, [f"Python syntax error: {e}"]

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base = alias.name.split(".")[0]
                        if base in self.blocked_python_modules:
                            violations.append(f"Blocked module import: {base}")

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        base = node.module.split(".")[0]
                        if base in self.blocked_python_modules:
                            violations.append(f"Blocked module import: {base}")

                if isinstance(node, ast.Call):
                    fn = node.func
                    if isinstance(fn, ast.Name) and fn.id in self.blocked_python_calls:
                        violations.append(f"Blocked function call: {fn.id}")
                    if isinstance(fn, ast.Attribute) and fn.attr in self.blocked_python_attrs:
                        violations.append(f"Blocked dangerous call: {fn.attr}")

        for pattern in self.blocked_patterns.get(language, []):
            if re.search(pattern, code, flags=re.IGNORECASE | re.MULTILINE):
                violations.append(f"Blocked pattern for {language}: {pattern}")

        return len(violations) == 0, violations

    def _execute_in_container(self, context: Dict[str, Any]) -> Dict[str, Any]:
        docker_client = self._get_docker_client()
        if docker_client is None or not self.docker_available:
            return {
                "output": "",
                "error": "Docker service is not available. Secure execution requires Docker.",
                "exit_code": -1,
                "execution_time": 0,
                "memory_used": 0,
            }

        code = context["code"]
        language = context["language"]
        input_data = context["input_data"]
        config = context["config"]

        with tempfile.TemporaryDirectory(prefix="openlearnx_exec_") as temp_dir:
            os.chmod(temp_dir, 0o755)
            code_path = os.path.join(temp_dir, config["file_name"])
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(code)
            os.chmod(code_path, 0o644)

            input_path = os.path.join(temp_dir, "input.txt")
            with open(input_path, "w", encoding="utf-8") as f:
                f.write(input_data)
            os.chmod(input_path, 0o644)

            container = None
            start = time.time()
            try:
                cpu_quota = int(float(config["cpu_limit"]) * 100000)
                container = docker_client.containers.run(
                    config["image"],
                    command=self._build_execution_command(config),
                    volumes={temp_dir: {"bind": "/workspace", "mode": "rw"}},
                    working_dir="/workspace",
                    mem_limit=config["memory_limit"],
                    memswap_limit=config["memory_limit"],
                    cpu_period=100000,
                    cpu_quota=cpu_quota,
                    pids_limit=64,
                    network_mode="none",
                    detach=True,
                    stdin_open=False,
                    tty=False,
                    cap_drop=["ALL"],
                    security_opt=["no-new-privileges:true"],
                    read_only=True,
                    user="65534:65534",
                    tmpfs={
                        "/tmp": "rw,noexec,nosuid,size=64m",
                    },
                    labels={
                        "openlearnx.sandbox": "true",
                        "openlearnx.execution_id": context["execution_id"],
                    },
                )

                wait_result = container.wait(timeout=config["timeout"] + 2)
                logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="replace")
                status_code = int(wait_result.get("StatusCode", -1))
                execution_time = round(time.time() - start, 3)
                memory_used = self._get_memory_usage(container)

                if status_code != 0:
                    return {
                        "output": "",
                        "error": self._sanitize_error_output(language, logs.strip() or f"Runtime exited with code {status_code}"),
                        "exit_code": status_code,
                        "execution_time": execution_time,
                        "memory_used": memory_used,
                    }

                return {
                    "output": logs.strip(),
                    "error": "",
                    "exit_code": 0,
                    "execution_time": execution_time,
                    "memory_used": memory_used,
                }

            except Exception as e:
                if container is not None:
                    try:
                        container.kill()
                    except Exception:
                        pass
                return {
                    "output": "",
                    "error": self._sanitize_error_output(language, f"Execution failed or timed out: {str(e)}"),
                    "exit_code": -1,
                    "execution_time": round(time.time() - start, 3),
                    "memory_used": 0,
                }
            finally:
                if container is not None:
                    try:
                        container.remove(force=True)
                    except Exception:
                        pass

    def _sanitize_error_output(self, language: str, raw_error: str) -> str:
        if not raw_error:
            return "Runtime error"

        text = str(raw_error)
        # Avoid leaking container-internal paths.
        text = re.sub(r"/workspace/", "", text)
        lines = [line.rstrip() for line in text.splitlines() if line.strip()]

        if language == "python":
            cleaned: List[str] = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("Traceback"):
                    continue
                if stripped.startswith("File "):
                    continue
                if stripped.startswith("^"):
                    continue
                cleaned.append(stripped)

            for line in reversed(cleaned):
                if "Error" in line or "Exception" in line:
                    return line
            if cleaned:
                return cleaned[-1]
            return "Python runtime error"

        # Keep non-python errors concise.
        tail = lines[-3:] if len(lines) > 3 else lines
        sanitized = "\n".join(tail).strip()
        return sanitized or "Runtime error"

    def _build_execution_command(self, config: Dict[str, Any]) -> str:
        commands: List[str] = []
        if config.get("compile_command"):
            commands.append(config["compile_command"])

        run_cmd = config["run_command"]
        if "< /workspace/input.txt" not in run_cmd:
            run_cmd = f"{run_cmd} < /workspace/input.txt"

        # ulimit adds an additional in-container CPU-time and file-size restriction.
        shell_cmd = " && ".join(commands + [run_cmd])
        return f"sh -c 'ulimit -t {config['timeout']} -f 1024; {shell_cmd} 2>&1'"

    def _get_memory_usage(self, container) -> int:
        try:
            stats = container.stats(stream=False)
            return int(stats.get("memory_stats", {}).get("usage", 0))
        except Exception:
            return 0

    def get_supported_languages(self) -> List[Dict[str, str]]:
        return [
            {
                "id": lang_id,
                "name": lang_id.title(),
                "extension": os.path.splitext(config["file_name"])[1],
                "timeout": config["timeout"],
                "memory_limit": config["memory_limit"],
            }
            for lang_id, config in self.language_configs.items()
        ]

    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        return self.active_executions.get(execution_id)

    def cancel_execution(self, execution_id: str) -> bool:
        if execution_id in self.active_executions:
            del self.active_executions[execution_id]
            return True
        return False


try:
    real_compiler_service = RealCompilerService()
except Exception as e:
    print(f"WARNING: Failed to initialize RealCompilerService: {e}")
    real_compiler_service = RealCompilerService()
