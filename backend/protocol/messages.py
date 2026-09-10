import json
from typing import Any


def encode_message(message: dict[str, Any]) -> bytes:
    return (json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8")


def decode_message(line: bytes) -> dict[str, Any]:
    value = json.loads(line.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Message must be a JSON object")
    return value


def ok_response(message_id: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    response = {"id": message_id, "status": "ok"}
    if data:
        response["data"] = data
    return response


def error_response(message_id: str, code: str, message: str) -> dict[str, Any]:
    return {
        "id": message_id,
        "status": "error",
        "error": {"code": code, "message": message},
    }
