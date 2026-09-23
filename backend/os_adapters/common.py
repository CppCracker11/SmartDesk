try:
    from pynput import keyboard as kb, mouse as ms
except ImportError:
    kb = None
    ms = None

MAP = {"ENTER":"enter","ESC":"esc","BACKSPACE":"backspace","TAB":"tab","SHIFT":"shift","CTRL":"ctrl","ALT":"alt","CMD":"cmd","SPACE":"space","UP":"up","DOWN":"down","LEFT":"left","RIGHT":"right","HOME":"home","END":"end","PAGEUP":"page_up","PAGEDOWN":"page_down","DELETE":"delete","INSERT":"insert","CAPSLOCK":"caps_lock","F1":"f1","F2":"f2","F3":"f3","F4":"f4","F5":"f5","F6":"f6","F7":"f7","F8":"f8","F9":"f9","F10":"f10","F11":"f11","F12":"f12"}

def req():
    if kb is None or ms is None:
        raise RuntimeError("pynput is not installed")
# Glossary:
# req = require pynput

def key(val):
    req()
    if len(val) == 1:
        return val
    nam = MAP.get(val.upper())
    if not nam:
        raise ValueError("unsupported key")
    return getattr(kb.Key, nam)
# Glossary:
# key = translate protocol key
# val = value
# nam = mapped name

def med():
    req()
    return {"play_pause": kb.Key.media_play_pause, "next": kb.Key.media_next, "previous": kb.Key.media_previous, "volume_up": kb.Key.media_volume_up, "volume_down": kb.Key.media_volume_down, "mute": kb.Key.media_volume_mute}
# Glossary:
# med = media key map
