import asyncio

from .connection import ClientConnection
from .discovery import start_discovery
from ..config import DISCOVERY_PORT, PORT, PROTOCOL_VERSION
from ..security.pairing import PairingManager
from ..security.session import SessionManager
from ..utils.system_info import get_host_info


class SmartDeskServer:
    def __init__(self, host, port, discovery_port, pairing_timeout, adapter, logger):
        self.host = host
        self.port = port
        self.discovery_port = discovery_port
        self.logger = logger
        self.pairing = PairingManager(pairing_timeout)
        self.session = SessionManager()
        self.adapter = adapter
        self.server = None
        self.discovery_transport = None
        self.dispatcher = None

    async def start(self):
        from ..commands.dispatcher import CommandDispatcher
        self.dispatcher = CommandDispatcher(self.adapter, self.logger)
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self.port = self.server.sockets[0].getsockname()[1]
        self.logger.info("SmartDesk server started")
        self.logger.info("Listening on %s:%s", self.host, self.port)
        self.logger.info("Pairing code: %s", self.pairing.get_code())

        loop = asyncio.get_running_loop()
        self.discovery_transport = await start_discovery(
            loop,
            self.discovery_port,
            lambda: self.discovery_response(),
            self.logger,
        )

    def discovery_response(self):
        info = get_host_info(self.port, PROTOCOL_VERSION)
        return {
            "type": "SMARTDESK_HOST",
            "hostname": info["hostname"],
            "ip": info["ip"],
            "port": self.port,
            "protocol_version": PROTOCOL_VERSION,
        }

    async def handle_client(self, reader, writer):
        info = get_host_info(self.port, PROTOCOL_VERSION)
        connection = ClientConnection(
            reader,
            writer,
            self.pairing,
            self.session,
            self.dispatcher,
            info,
            self.logger,
        )
        await connection.run()

    async def run_forever(self):
        await self.start()
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.discovery_transport:
            self.discovery_transport.close()
        if self.server:
            self.server.close()
            await self.server.wait_closed()
