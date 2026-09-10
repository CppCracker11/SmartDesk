import asyncio
import json


class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self, response_factory, logger):
        self.response_factory = response_factory
        self.logger = logger
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if data.decode("utf-8", errors="ignore").strip() != "SMARTDESK_DISCOVER":
            return
        response = json.dumps(self.response_factory()).encode("utf-8")
        self.transport.sendto(response, addr)
        self.logger.info("Discovery response sent to %s", addr[0])

    def error_received(self, exc):
        self.logger.error("Discovery error: %s", exc)


async def start_discovery(loop, port, response_factory, logger):
    transport, _ = await loop.create_datagram_endpoint(
        lambda: DiscoveryProtocol(response_factory, logger),
        local_addr=("0.0.0.0", port),
        allow_broadcast=True,
    )
    logger.info("UDP discovery listening on port %s", port)
    return transport
