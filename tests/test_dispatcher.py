import unittest

from backend.commands.dispatcher import CommandDispatcher


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def mouse_move(self, dx, dy): self.calls.append(("move", dx, dy))
    def mouse_click(self, button): self.calls.append(("click", button))
    def mouse_double_click(self): self.calls.append(("double",))
    def mouse_scroll(self, dx, dy): self.calls.append(("scroll", dx, dy))
    def key_press(self, key): self.calls.append(("press", key))
    def key_release(self, key): self.calls.append(("release", key))
    def key_combo(self, keys): self.calls.append(("combo", keys))
    def media_control(self, action): self.calls.append(("media", action))
    def presentation_control(self, action): self.calls.append(("presentation", action))


class DispatcherTests(unittest.TestCase):
    def test_mouse_dispatch(self):
        adapter = FakeAdapter()
        dispatcher = CommandDispatcher(adapter, type("L", (), {"info": lambda *x: None, "error": lambda *x: None})())
        response = dispatcher.dispatch({"id": "1", "type": "mouse", "action": "move", "data": {"dx": 3, "dy": 4}})
        self.assertEqual(response["status"], "ok")
        self.assertEqual(adapter.calls, [("move", 3, 4)])


if __name__ == "__main__":
    unittest.main()
