import os
import re
import subprocess
import sys
from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, conversation_history
from services.ollama_service import send_messages_to_ollama
from core.rikaa import process_user_request


_GENERATED_DIR = "generated"
_OUTPUT_FILE = "output.py"

router = APIRouter()

# Keywords that suggest the user is asking for code
_CODE_KEYWORDS = {
    "create", "write", "generate", "make", "build", "implement",
    "code", "program", "script", "function", "class", "method",
}


def _is_code_request(message: str) -> bool:
    """Heuristically determine if the user is asking for code."""
    words = set(message.lower().split())
    return bool(words & _CODE_KEYWORDS)


def _extract_code_block(text: str) -> str:
    """Extract the first fenced code block from text, or return empty string."""
    match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def _save_code_to_file(code: str) -> str:
    """Save code to backend/generated/output.py. Returns the relative path."""
    os.makedirs(_GENERATED_DIR, exist_ok=True)
    filepath = os.path.join(_GENERATED_DIR, _OUTPUT_FILE)
    with open(filepath, "w") as f:
        f.write(code)
    return filepath


def _run_generated_file() -> dict | None:
    """Execute generated/output.py and return run result, or None if file missing."""
    filepath = os.path.join(_GENERATED_DIR, _OUTPUT_FILE)
    if not os.path.isfile(filepath):
        return None

    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out after 30 seconds.",
            "exit_code": -1,
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "exit_code": -1,
        }


@router.post("/chat")
def chat_with_ai(request: ChatRequest):

    # Pass through RIKAA Core layer — returns [system, user]
    try:
        core_messages = process_user_request(request.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    system_message = core_messages[0]
    user_message = core_messages[1]

    # Build full message list: system + conversation_history + current user
    ollama_messages = [system_message] + conversation_history + [user_message]

    # Send to Ollama
    assistant_reply = send_messages_to_ollama(ollama_messages)

    # Append current turn to conversation history
    conversation_history.append(user_message)
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # Extract code if applicable
    code = _extract_code_block(assistant_reply) if _is_code_request(request.message) else ""

    # Save to file if code is non-empty
    file_path = _save_code_to_file(code) if code else ""

    # Execute if a file was written
    run_result = _run_generated_file() if file_path else None

    # Derive build status from run result
    if run_result is not None:
        build_success = run_result["exit_code"] == 0
        build_result = {
            "success": build_success,
            "message": "Build completed successfully." if build_success else "Build failed.",
        }
    else:
        build_result = None

    return {
        "reply": assistant_reply,
        "code": code,
        "file": file_path,
        "run": run_result,
        "build": build_result,
    }
