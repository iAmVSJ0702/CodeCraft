import os
import sys
import random
import tempfile
import subprocess
import requests
from io import StringIO
from datetime import datetime
from typing import Tuple
import contextlib

# --- Utility context manager to capture stdout/stderr (for Python execution) ---
@contextlib.contextmanager
def capture_output():
    stdout, stderr = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = stdout, stderr
        yield stdout, stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

# --- Public API to execute code ---
def execute_code(code: str, stdin: str = "", language: str = "cpp") -> Tuple[str, str, str]:
    try:
        if language == "Python":
            return _execute_python(code, stdin)
        elif language == "C":
            return _execute_c(code, stdin)
        elif language == "C++":
            return _execute_cpp(code, stdin)
        elif language == "Java":
            return _execute_with_onecompiler(code, stdin, language="java", filename="Main.java")
        elif language == "JavaScript":
            return _execute_with_onecompiler(code, stdin, language="javascript", filename="script.js")
        elif language == "C#":
            return _execute_with_onecompiler(code, stdin, language="csharp", filename="Program.cs")
        else:
            return "", f"Unsupported language: {language}", None
    except Exception as e:
        return "", "", str(e)

# --- Python Execution ---
def _execute_python(code: str, stdin: str) -> Tuple[str, str, str]:
    with capture_output() as (stdout, stderr):
        try:
            inputs = iter(stdin.splitlines())
            input_override = lambda prompt='': next(inputs, '')
            local_vars = {"input": input_override}
            exec(code, {}, local_vars)
            return stdout.getvalue().strip(), stderr.getvalue().strip(), None
        except Exception as e:
            return stdout.getvalue().strip(), stderr.getvalue().strip(), str(e)

# --- C Execution ---
def _execute_c(code: str, stdin: str):
    return _compile_and_run(code, stdin, ext="c", compiler="gcc")

# --- C++ Execution ---
def _execute_cpp(code: str, stdin: str):
    return _compile_and_run(code, stdin, ext="cpp", compiler="g++")

# --- Compilation helper ---
def _compile_and_run(code: str, stdin: str, ext: str, compiler: str):
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, f"main.{ext}")
        binary = os.path.join(tmp, "main.out")

        with open(source, "w") as f:
            f.write(code)

        compile_cmd = [compiler, source, "-o", binary]
        comp_out, comp_err, comp_exc = _run_subprocess(compile_cmd)

        if comp_exc or comp_err:
            return comp_out, comp_err, comp_exc

        return _run_subprocess([binary], stdin)

# --- Run subprocess and capture output ---
def _run_subprocess(cmd, stdin_input=None) -> Tuple[str, str, str]:
    try:
        result = subprocess.run(
            cmd,
            input=stdin_input.encode() if stdin_input else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        return result.stdout.decode(), result.stderr.decode(), None
    except Exception as e:
        return "", "", str(e)

# --- Java, JS, C# via OneCompiler API ---
def _execute_with_onecompiler(code: str, stdin: str, language: str, filename: str) -> Tuple[str, str, str]:
    keys = [os.environ["ONECOMPILER_API_KEY"], os.environ["ONECOMPILER_API_KEY1"]]
    primary_key = random.choice(keys)

    result = _call_onecompiler_api(primary_key, code, stdin, language, filename)

    if _is_quota_or_invalid(result):
        for key in keys:
            if key == primary_key:
                continue
            result = _call_onecompiler_api(key, code, stdin, language, filename)
            if not _is_quota_or_invalid(result):
                break

    return result

def _call_onecompiler_api(key: str, code: str, stdin: str, language: str, filename: str) -> Tuple[str, str, str]:
    url = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
        "x-rapidapi-key": key,
    }
    payload = {
        "language": language.lower(),
        "stdin": stdin,
        "files": [{"name": filename, "content": code}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()

        if data.get("status") == "failed":
            return "", "", f"OneCompiler Error: {data.get('error')}"

        return (
            data.get("stdout", "").strip(),
            data.get("stderr", "") or "",
            data.get("exception", "")
        )
    except Exception as e:
        return "", "", str(e)

def _is_quota_or_invalid(result: Tuple[str, str, str]) -> bool:
    _, _, error = result
    if not error:
        return False
    error = error.lower()
    return any(term in error for term in ["quota", "e002", "e003", "invalid", "exhausted"])

# --- Export utility ---
def export_session(code: str, output: str, error: str) -> dict:
    return {
        "timestamp": datetime.now().isoformat(),
        "code": code,
        "output": output,
        "error": error
    }
