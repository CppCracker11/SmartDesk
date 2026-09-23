import time as tim

class Cmd:
    def __init__(self, adp, log):
        self.adp = adp
        self.log = log

    def run(self, msg):
        mid, typ, act = msg["id"], msg["type"], msg["action"]
        dat = msg.get("data", {})
        ts = tim.perf_counter()
        try:
            if typ == "mouse": self.mou(act, dat)
            elif typ == "keyboard": self.key(act, dat)
            elif typ == "media": self.adp.med(act)
            elif typ == "presentation": self.adp.pre(act)
            else: return {"id": mid, "status": "error", "error": {"code": "INVALID_COMMAND", "message": "command is not executable"}}
        except (ValueError, KeyError, TypeError) as exc:
            self.log.error("command failed: %s", exc)
            return {"id": mid, "status": "error", "error": {"code": "INVALID_PARAMETER", "message": "invalid command parameter"}}
        except Exception as exc:
            self.log.error("adapter command failed: %s", exc)
            return {"id": mid, "status": "error", "error": {"code": "COMMAND_FAILED", "message": "input control failed"}}
        ms = (tim.perf_counter() - ts) * 1000
        return {"id": mid, "status": "ok", "data": {"processing_ms": round(ms, 3)}}
    # Glossary:
    # Cmd = command dispatcher
    # run = dispatch command
    # adp = adapter
    # log = logger
    # msg = message
    # mid = message id
    # typ = type
    # act = action
    # dat = data
    # ts = start time
    # ms = milliseconds

    def mou(self, act, dat):
        if act == "move": self.adp.mov(dat["dx"], dat["dy"])
        elif act in {"left_click", "right_click", "middle_click"}: self.adp.clk(act[:-6])
        elif act == "double_click": self.adp.dbl()
        elif act == "scroll": self.adp.scr(dat.get("dx", 0), dat.get("dy", 0))
        else: raise ValueError("invalid mouse action")
    # Glossary:
    # mou = mouse dispatch

    def key(self, act, dat):
        if act == "press": self.adp.prs(dat["key"])
        elif act == "release": self.adp.rel(dat["key"])
        elif act == "combo": self.adp.cmb(dat["keys"])
        else: raise ValueError("invalid keyboard action")
    # Glossary:
    # key = keyboard dispatch
