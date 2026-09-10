from .base import OSAdapter
from .common import keyboard, mouse, pynput_key, require_pynput


class MacOSAdapter(OSAdapter):
    def __init__(self):
        require_pynput()
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def mouse_move(self, dx, dy):
        self.mouse_controller.move(dx, dy)

    def mouse_click(self, button):
        self.mouse_controller.click(getattr(mouse.Button, button), 1)

    def mouse_double_click(self):
        self.mouse_controller.click(mouse.Button.left, 2)

    def mouse_scroll(self, dx, dy):
        self.mouse_controller.scroll(dx, dy)

    def key_press(self, key):
        self.keyboard_controller.press(pynput_key(key))

    def key_release(self, key):
        self.keyboard_controller.release(pynput_key(key))

    def key_combo(self, keys):
        pressed = [pynput_key(key) for key in keys]
        try:
            for key in pressed:
                self.keyboard_controller.press(key)
        finally:
            for key in reversed(pressed):
                self.keyboard_controller.release(key)

    def media_control(self, action):
        media = {
            "play_pause": keyboard.Key.media_play_pause,
            "next": keyboard.Key.media_next,
            "previous": keyboard.Key.media_previous,
            "volume_up": keyboard.Key.media_volume_up,
            "volume_down": keyboard.Key.media_volume_down,
            "mute": keyboard.Key.media_volume_mute,
        }
        self.keyboard_controller.press(media[action])
        self.keyboard_controller.release(media[action])

    def presentation_control(self, action):
        self.key_press("RIGHT" if action == "next" else "LEFT")
