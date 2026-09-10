try:
    from pynput import keyboard, mouse
except ImportError:
    keyboard = None
    mouse = None


KEY_MAP = {
    "ENTER": "enter", "ESC": "esc", "BACKSPACE": "backspace", "TAB": "tab",
    "SHIFT": "shift", "CTRL": "ctrl", "ALT": "alt", "SPACE": "space",
    "UP": "up", "DOWN": "down", "LEFT": "left", "RIGHT": "right",
    "HOME": "home", "END": "end", "PAGEUP": "page_up", "PAGEDOWN": "page_down",
    "DELETE": "delete", "INSERT": "insert", "CAPSLOCK": "caps_lock",
    "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5", "F6": "f6",
    "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12",
}


def require_pynput() -> None:
    if keyboard is None or mouse is None:
        raise RuntimeError("pynput is not installed")


def pynput_key(key: str):
    require_pynput()
    upper = key.upper()
    if len(key) == 1:
        return key
    name = KEY_MAP.get(upper)
    if not name:
        raise ValueError("Unsupported key")
    return getattr(keyboard.Key, name)
