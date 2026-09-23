TYP = {
    "auth": {"pair", "resume"},
    "mouse": {"move", "left_click", "right_click", "double_click", "middle_click", "scroll"},
    "keyboard": {"press", "release", "combo"},
    "media": {"play_pause", "next", "previous", "volume_up", "volume_down", "mute"},
    "presentation": {"next", "previous"},
    "system": {"ping", "get_host_info", "disconnect"},
}
KEY = {"ENTER","ESC","BACKSPACE","TAB","SHIFT","CTRL","ALT","CMD","SPACE","UP","DOWN","LEFT","RIGHT","HOME","END","PAGEUP","PAGEDOWN","DELETE","INSERT","CAPSLOCK","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"}

def num(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)
# Glossary:
# num = number check
# val = value

def key(val):
    if not isinstance(val, str) or len(val) > 32 or not val:
        return False
    up = val.upper()
    return len(val) == 1 and val.isprintable() or up in KEY
# Glossary:
# key = key validation
# up = uppercase key

def val(msg):
    if not isinstance(msg, dict):
        return False, "INVALID_MESSAGE", "message must be an object"
    if msg.get("version") != "1.0":
        return False, "UNSUPPORTED_VERSION", "unsupported protocol version"
    if not isinstance(msg.get("id"), str) or not msg["id"] or len(msg["id"]) > 128:
        return False, "INVALID_MESSAGE", "id must be a non-empty string"
    typ, act = msg.get("type"), msg.get("action")
    if not isinstance(typ, str) or not isinstance(act, str):
        return False, "INVALID_MESSAGE", "type and action are required"
    if typ not in TYP or act not in TYP[typ]:
        return False, "INVALID_COMMAND", "unknown command"
    dat = msg.get("data", {})
    if not isinstance(dat, dict):
        return False, "INVALID_PARAMETER", "data must be an object"
    if typ == "mouse" and act == "move":
        if not num(dat.get("dx")) or not num(dat.get("dy")):
            return False, "INVALID_PARAMETER", "dx and dy must be numbers"
        if abs(dat["dx"]) > 2000 or abs(dat["dy"]) > 2000:
            return False, "INVALID_PARAMETER", "mouse movement is out of range"
    if typ == "mouse" and act == "scroll":
        if not num(dat.get("dx", 0)) or not num(dat.get("dy", 0)):
            return False, "INVALID_PARAMETER", "scroll values must be numbers"
        if abs(dat.get("dx", 0)) > 50 or abs(dat.get("dy", 0)) > 50:
            return False, "INVALID_PARAMETER", "scroll value is out of range"
    if typ == "keyboard" and act in {"press", "release"} and not key(dat.get("key")):
        return False, "INVALID_PARAMETER", "unsupported key"
    if typ == "keyboard" and act == "combo":
        ks = dat.get("keys")
        if not isinstance(ks, list) or not 1 <= len(ks) <= 6 or not all(key(x) for x in ks):
            return False, "INVALID_PARAMETER", "keys must contain 1 to 6 supported keys"
    if typ == "auth" and act == "pair":
        cod = dat.get("code")
        if not isinstance(cod, str) or len(cod) != 6 or not cod.isdigit():
            return False, "INVALID_PARAMETER", "pairing code must be six digits"
    if typ == "auth" and act == "resume":
        tok = dat.get("token")
        if not isinstance(tok, str) or len(tok) < 16:
            return False, "INVALID_PARAMETER", "session token is required"
    return True, "", ""
# Glossary:
# val = validate
# msg = message
# typ = type
# act = action
# dat = data
# ks = keys
# tok = token
# cod = code
