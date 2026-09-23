import asyncio as aio
from .connection import Con
from .discovery import new
from ..config import DPT, PRT, VER
from ..security.pairing import Pai
from ..security.session import Ses
from ..utils.system_info import inf
from ..commands.dispatcher import Cmd

class Srv:
    def __init__(self, hst, prt, dpt, pto, adp, log):
        self.hst, self.prt, self.dpt, self.log = hst, prt, dpt, log
        self.pai, self.ses, self.adp = Pai(pto), Ses(), adp
        self.srv, self.dtr, self.cmd = None, None, None

    async def sta(self):
        self.cmd = Cmd(self.adp, self.log)
        self.srv = await aio.start_server(self.cli, self.hst, self.prt)
        self.prt = self.srv.sockets[0].getsockname()[1]
        loop = aio.get_running_loop()
        try:
            self.dtr = await new(loop, self.dpt, self.dis, self.log)
        except OSError as exc:
            self.log.warning("UDP discovery unavailable: %s", exc)
        self.log.info("SmartDesk TCP listening on %s:%s", self.hst, self.prt)
        self.log.info("Pairing code: %s", self.pai.get())
    # Glossary:
    # sta = start
    # hst = host
    # prt = port
    # dpt = discovery port
    # pto = pairing timeout
    # adp = adapter
    # log = logger

    def dis(self):
        x = inf(self.prt, VER)
        return {"type":"SMARTDESK_HOST","hostname":x["hostname"],"ip":x["ip"],"port":self.prt,"protocol_version":VER}
    # Glossary:
    # dis = discovery response
    # x = host info

    async def cli(self, rdr, wtr):
        x = inf(self.prt, VER)
        con = Con(rdr, wtr, self.pai, self.ses, self.cmd, x, self.log)
        await con.run()
    # Glossary:
    # cli = client handler
    # rdr = reader
    # wtr = writer
    # con = connection

    async def run(self):
        await self.sta()
        async with self.srv: await self.srv.serve_forever()
    # Glossary:
    # run = serve forever

    async def end(self):
        if self.dtr: self.dtr.close()
        if self.srv:
            self.srv.close(); await self.srv.wait_closed()
    # Glossary:
    # end = stop server
