import asyncio as aio
from .config import HST, PRT, DPT, PTO, LOG, STO
from .os_adapters.factory import new
from .network.server import Srv
from .utils.logging import log as lg

async def go():
    log = lg(LOG)
    try: adp = new()
    except Exception as exc:
        log.error("Input adapter could not start: %s", exc); return
    srv = Srv(HST, PRT, DPT, PTO, adp, log)
    srv.ses.tmo = STO
    try: await srv.run()
    except KeyboardInterrupt: pass
    finally: await srv.end()
# Glossary:
# main = application entry
# log = logger
# adp = adapter
# srv = server

if __name__ == "__main__": aio.run(go())
