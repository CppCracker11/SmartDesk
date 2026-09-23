import asyncio as aio
import json as js

class Dis(aio.DatagramProtocol):
    def __init__(self, fac, log):
        self.fac, self.log, self.trn = fac, log, None

    def mad(self, trn): self.trn = trn
    # Glossary:
    # mad = connection made
    # trn = transport

    def got(self, dat, adr):
        if dat.decode("utf-8", "ignore").strip() != "SMARTDESK_DISCOVER": return
        self.trn.sendto(js.dumps(self.fac(), separators=(",", ":")).encode(), adr)
    # Glossary:
    # dat = datagram
    # adr = address

    def bad(self, exc): self.log.error("discovery error: %s", exc)
    # Glossary:
    # bad = error callback
    # exc = exception

setattr(Dis, "connection_made", Dis.mad)
setattr(Dis, "datagram_received", Dis.got)
setattr(Dis, "error_received", Dis.bad)

async def new(loop, prt, fac, log):
    trn, _ = await loop.create_datagram_endpoint(lambda: Dis(fac, log), local_addr=("0.0.0.0", prt), allow_broadcast=True)
    return trn
# Glossary:
# new = start discovery
# loop = event loop
# prt = port
# fac = response factory
