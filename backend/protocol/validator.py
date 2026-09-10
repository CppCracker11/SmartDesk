from typing import Any

ALLOWED_TYPES = {
    "auth": {"pair", "resume"},
    "mouse": {"move", "left_click", "right_click", "double_click", "middle_click", "scroll"},
    "keyboard": {"press", "release", "combo"},
    "media": {"play_pause", "next", "previous", "volume_up", "volume_down", "mute"},
    "presentation": {"next", "previous"},
    "system": {"ping", "get_host_info", "disconnect"},
}

ALLOWED_KEYS = {
    "ENTER", "ESC", "BACKSPACE", "TAB", "SHIFT", "CTRL", "ALT", "SPACE",
    "UP", "DOWN", "LEFT", "RIGHT", "HOME", "END", "PAGEUP", "PAGEDOWN",
    "DELETE", "INSERT", "CAPSLOCK", "F1", "F2", "F3", "F4", "F5", "F6",
    "F7", "F8", "F9", "F10", "F11", "F12",
}


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_message(message: dict[str, Any]) -> tuple[bool, str, str]:
    if message.get("version") != "1.0":
        return False, "UNSUPPORTED_VERSION", "Unsupported protocol version"
    if not isinstance(message.get("id"), str) or not message["id"]:
        return False, "INVALID_ID", "Message id must be a non-empty string"
    if not isinstance(message.get("type"), str) or not isinstance(message.get("action"), str):
        return False, "INVALID_MESSAGE", "type and action are required"

    msg_type = message["type"]
    action = message["action"]
    if msg_type not in ALLOWED_TYPES or action not in ALLOWED_TYPES[msg_type]:
        return False, "INVALID_COMMAND", "Unknown command"

    data = message.get("data", {})
    if not isinstance(data, dict):
        return False, "INVALID_DATA", "data must be an object"

    if msg_type == "mouse" and action == "move":
        if not _number(data.get("dx")) or not _number(data.get("dy")):
            return False, "INVALID_DATA", "dx and dy must be numbers"
        if abs(data["dx"]) > 2000 or abs(data["dy"]) > 2000:
            return False, "INVALID_DATA", "mouse movement is out of range"

    if msg_type == "mouse" and action == "scroll":
        if not _number(data.get("dx", 0)) or not _number(data.get("dy", 0)):
            return False, "INVALID_DATA", "scroll values must be numbers"
        if abs(data.get("dx", 0)) > 50 or abs(data.get("dy", 0)) > 50:
            return False, "INVALID_DATA", "scroll value is out of range"

    if msg_type == "keyboard" and action in {"press", "release"}:
        key = data.get("key")
        if not isinstance(key, str) or len(key) > 32:
            return False, "INVALID_DATA", "key must be a short string"
        upper = key.upper()
        if len(key) == 1 and key.isprintable():
            pass
        elif upper not in ALLOWED_KEYS:
            return False, "INVALID_DATA", "unsupported key"

    if msg_type == "keyboard" and action == "combo":
        keys = data.get("keys")
        if not isinstance(keys, list) or not keys or len(keys) > 6:
            return False, "INVALID_DATA", "keys must be a list of 1 to 6 keys"
        for key in keys:
            if not isinstance(key, str):
                return False, "INVALID_DATA", "each key must be a string"
            if len(key) != 1 and key.upper() not in ALLOWED_KEYS:
                return False, "INVALID_DATA", "unsupported key in combination"

    if msg_type == "auth" and action == "pair":
        if not isinstance(data.get("code"), str) or len(data["code"]) != 6 or not data["code"].isdigit():
            return False, "INVALID_DATA", "pairing code must be six digits"
    if msg_type == "auth" and action == "resume":
        if not isinstance(data.get("token"), str) or len(data["token"]) < 16:
            return False, "INVALID_DATA", "session token is required"

    return True, "", ""
