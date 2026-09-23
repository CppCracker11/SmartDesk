import asyncio as aio
import time as tim
from ..protocol.messages import enc, ok, err
from ..protocol.parser import Pro
from ..protocol.validator import val

class Con:
    def __init__(self, rdr, wtr, pai, ses, cmd, inf, log):
        self.rdr, self.wtr, self.pai, self.ses = rdr, wtr, pai, ses
        self.cmd, self.inf, self.log = cmd, inf, log
        self.aut = False
        self.tok = None
        self.cid = id(self)
        self.pro = Pro()
        self.sta = "CONNECTING"

    async def snd(self, msg):
        self.wtr.write(enc(msg))
        await self.wtr.drain()
    # Glossary:
    # snd = send
    # msg = message

    async def run(self):
        self.sta = "CONNECTED"
        await self.snd({"type": "state", "state": "AUTHENTICATING"})
        try:
            while True:
                dat = await self.rdr.read(4096)
                if not dat:
                    break
                try:
                    msgs = self.pro.fed(dat)
                except ValueError as exc:
                    cod = "INVALID_JSON" if str(exc) == "invalid json" else "INVALID_MESSAGE"
                    await self.snd(err("", cod, "invalid SmartDesk message"))
                    break
                for msg in msgs:
                    await self.msg(msg)
        except (aio.CancelledError, ConnectionError, BrokenPipeError):
            pass
        except Exception as exc:
            self.log.error("connection error: %s", exc)
        finally:
            self.sta = "DISCONNECTED"
            self.ses.rel(self.tok, self.cid)
            self.wtr.close()
            try:
                await self.wtr.wait_closed()
            except Exception:
                pass
    # Glossary:
    # run = connection loop
    # dat = bytes
    # msgs = messages
    # msg = message
    # exc = exception

    async def msg(self, msg):
        try:
            good, cod, txt = val(msg)
        except Exception:
            good, cod, txt = False, "INVALID_MESSAGE", "invalid message"
        mid = msg.get("id", "") if isinstance(msg, dict) else ""
        if not good:
            await self.snd(err(mid, cod, txt))
            return
        typ, act = msg["type"], msg["action"]
        if not self.aut:
            if typ != "auth":
                await self.snd(err(mid, "NOT_AUTHENTICATED", "authenticate before sending commands"))
                return
            if act == "pair":
                if self.ses.has():
                    await self.snd(err(mid, "HOST_BUSY", "another controller is active"))
                    return
                if not self.pai.ver(msg["data"]["code"]):
                    await self.snd(err(mid, "PAIRING_FAILED", "pairing failed"))
                    return
                self.tok = self.ses.new(self.cid)
                self.aut = True
                self.sta = "ACTIVE"
                await self.snd(ok(mid, {"token": self.tok, "state": self.sta})); return
            if act == "resume":
                tok = msg["data"]["token"]
                if not self.ses.ok(tok):
                    await self.snd(err(mid, "SESSION_EXPIRED", "session token is invalid or expired")); return
                if self.ses.act:
                    await self.snd(err(mid, "HOST_BUSY", "another controller is active")); return
                if not self.ses.use(tok, self.cid):
                    await self.snd(err(mid, "SESSION_EXPIRED", "session token is invalid or expired")); return
                self.tok = tok
                self.aut = True
                self.sta = "ACTIVE"
                await self.snd(ok(mid, {"token": tok, "state": self.sta})); return
        tok = msg.get("token")
        if not tok or not self.ses.ok(tok) or tok != self.tok or not self.ses.act:
            await self.snd(err(mid, "SESSION_EXPIRED", "session token is invalid or expired")); return
        if typ == "system":
            if act == "ping":
                await self.snd(ok(mid, {"pong_ns": tim.time_ns()})); return
            if act == "get_host_info":
                await self.snd(ok(mid, self.inf)); return
            if act == "disconnect":
                await self.snd(ok(mid)); self.wtr.close(); return
        res = self.cmd.run(msg)
        await self.snd(res)
    # Glossary:
    # msg = message
    # good = validation result
    # cod = error code
    # txt = error text
    # mid = message id
    # typ = type
    # act = action
    # tok = token
    # res = response
