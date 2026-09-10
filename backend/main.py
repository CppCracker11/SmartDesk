import asyncio

from .config import DISCOVERY_PORT, HOST, LOG_LEVEL, PAIRING_TIMEOUT, PORT
from .os_adapters.factory import create_adapter
from .network.server import SmartDeskServer
from .utils.logging import setup_logging


async def main():
    logger = setup_logging(LOG_LEVEL)
    try:
        adapter = create_adapter()
    except Exception as exc:
        logger.error("Input adapter could not start: %s", exc)
        return

    server = SmartDeskServer(HOST, PORT, DISCOVERY_PORT, PAIRING_TIMEOUT, adapter, logger)
    try:
        await server.run_forever()
    except KeyboardInterrupt:
        logger.info("Stopping SmartDesk")
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
