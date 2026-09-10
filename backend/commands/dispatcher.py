import time


class CommandDispatcher:
    def __init__(self, adapter, logger):
        self.adapter = adapter
        self.logger = logger

    def dispatch(self, message: dict) -> dict:
        msg_id = message["id"]
        msg_type = message["type"]
        action = message["action"]
        data = message.get("data", {})
        started = time.perf_counter()

        try:
            if msg_type == "mouse":
                self._mouse(action, data)
            elif msg_type == "keyboard":
                self._keyboard(action, data)
            elif msg_type == "media":
                self.adapter.media_control(action)
            elif msg_type == "presentation":
                self.adapter.presentation_control(action)
            else:
                return {"id": msg_id, "status": "error", "error": {"code": "UNSUPPORTED_COMMAND", "message": "Command is not executable"}}
        except Exception as exc:
            self.logger.error("Command failed: %s", exc)
            return {"id": msg_id, "status": "error", "error": {"code": "OS_ERROR", "message": "Input control failed"}}

        elapsed = (time.perf_counter() - started) * 1000
        self.logger.info("Command: %s_%s (%.2f ms)", msg_type.upper(), action.upper(), elapsed)
        return {"id": msg_id, "status": "ok", "data": {"processing_ms": round(elapsed, 3)}}

    def _mouse(self, action, data):
        if action == "move":
            self.adapter.mouse_move(data["dx"], data["dy"])
        elif action in {"left_click", "right_click", "middle_click"}:
            self.adapter.mouse_click(action.replace("_click", ""))
        elif action == "double_click":
            self.adapter.mouse_double_click()
        elif action == "scroll":
            self.adapter.mouse_scroll(data.get("dx", 0), data.get("dy", 0))

    def _keyboard(self, action, data):
        if action == "press":
            self.adapter.key_press(data["key"])
        elif action == "release":
            self.adapter.key_release(data["key"])
        elif action == "combo":
            self.adapter.key_combo(data["keys"])
