import asyncio as aio
import platform
import time
from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal

from backend.config import HST, PRT, DPT, PTO, STO, VER
from backend.network.connection import Con
from backend.network.server import Srv
from backend.os_adapters.factory import new as new_adapter
from backend.utils.logging import log as setup_log
from backend.utils.system_info import inf


@dataclass(frozen=True)
class HostSettings:
    tcp_port: int = PRT
    discovery_port: int = DPT
    pairing_timeout: int = PTO
    session_timeout: int = STO


class DesktopServer(Srv):
    def __init__(self, *args, peer_changed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.peer_changed = peer_changed
        self.peers = {}

    async def cli(self, rdr, wtr):
        peer = wtr.get_extra_info("peername")
        peer_host = peer[0] if isinstance(peer, tuple) and peer else "Unknown"
        info = inf(self.prt, VER)
        con = Con(rdr, wtr, self.pai, self.ses, self.cmd, info, self.log)
        self.peers[con.cid] = peer_host
        if self.peer_changed:
            self.peer_changed()
        try:
            await con.run()
        finally:
            self.peers.pop(con.cid, None)
            if self.peer_changed:
                self.peer_changed()

    def controller_ip(self):
        if self.ses.cid is None:
            return None
        return self.peers.get(self.ses.cid)

    def peer_count(self):
        return len(self.peers)


class HostController(QObject):
    snapshot_changed = Signal(object)
    log_message = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.settings = HostSettings()
        self.server = None
        self.running = False
        self._started_at = None
        self._adapter_error = None

    async def start(self, settings=None):
        if self.running:
            return

        if settings is not None:
            self.settings = settings

        try:
            adapter = new_adapter()
            if adapter.__class__.__name__ == "Nul":
                raise RuntimeError("The local input backend is unavailable. Install pynput and restart SmartDesk.")

            log = setup_log("INFO")
            server = DesktopServer(
                HST,
                self.settings.tcp_port,
                self.settings.discovery_port,
                self.settings.pairing_timeout,
                adapter,
                log,
                peer_changed=self._emit_snapshot,
            )
            server.ses.tmo = self.settings.session_timeout
            await server.sta()
            self.server = server
            self.running = True
            self._started_at = time.monotonic()
            self._emit_snapshot()
            self.log_message.emit(f"SmartDesk host started on TCP {server.prt} / UDP {server.dpt}.")
        except Exception as exc:
            self.running = False
            self.server = None
            self._started_at = None
            self.error.emit(str(exc))
            raise

    async def stop(self):
        if self.server is not None:
            self.server.ses.clr()
            await self.server.end()
        self.server = None
        self.running = False
        self._started_at = None
        self._emit_snapshot()

    async def restart(self, settings):
        await self.stop()
        await self.start(settings)

    def snapshot(self):
        if not self.running or self.server is None:
            return {
                "running": False,
                "active": False,
                "waiting": False,
                "pairing_code": None,
                "pairing_remaining": 0,
                "tcp_port": self.settings.tcp_port,
                "discovery_port": self.settings.discovery_port,
                "hostname": platform.node(),
                "ip": "—",
                "os": platform.system(),
                "os_version": platform.release(),
                "peer_count": 0,
                "controller_ip": None,
                "uptime": 0,
            }

        active = self.server.ses.has()
        pairing_code = None
        pairing_remaining = 0

        if not active:
            pairing_code = self.server.pai.get()
            pairing_remaining = max(
                0,
                int(self.server.pai.tmo - (time.monotonic() - self.server.pai.ts)),
            )

        info = inf(self.server.prt, VER)
        return {
            "running": True,
            "active": active,
            "waiting": bool(self.server.peer_count()),
            "pairing_code": pairing_code,
            "pairing_remaining": pairing_remaining,
            "tcp_port": self.server.prt,
            "discovery_port": self.server.dpt,
            "hostname": info["hostname"],
            "ip": info["ip"],
            "os": info["os"],
            "os_version": info["os_version"],
            "peer_count": self.server.peer_count(),
            "controller_ip": self.server.controller_ip(),
            "uptime": max(0, int(time.monotonic() - self._started_at)) if self._started_at else 0,
        }

    def _emit_snapshot(self):
        self.snapshot_changed.emit(self.snapshot())
