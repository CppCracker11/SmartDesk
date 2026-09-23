import asyncio as aio
import json as js
import unittest as uni
from backend.network.server import Srv
from backend.utils.logging import log

class Fak:
    def mov(self,x,y): pass
    def clk(self,x): pass
    def dbl(self): pass
    def scr(self,x,y): pass
    def prs(self,x): pass
    def rel(self,x): pass
    def cmb(self,x): pass
    def med(self,x): pass
    def pre(self,x): pass

async def rd(r): return js.loads((await r.readline()).decode())

class ST(uni.TestCase):
    def t01(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r,w=await aio.open_connection("127.0.0.1",srv.prt); self.assertEqual((await rd(r))["state"],"AUTHENTICATING")
            m={"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":srv.pai.get()}}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); res=await rd(r); self.assertEqual(res["status"],"ok"); tok=res["data"]["token"]
            m={"version":"1.0","id":"2","type":"system","action":"ping","data":{},"token":tok}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); res=await rd(r); self.assertEqual(res["status"],"ok"); self.assertIn("pong_ns",res["data"])
            m={"version":"1.0","id":"3","type":"keyboard","action":"press","data":{"key":"ENTER"},"token":tok}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); self.assertEqual((await rd(r))["status"],"ok")
            w.close(); await w.wait_closed(); await srv.end()
        aio.run(run())

    def t04(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r,w=await aio.open_connection("127.0.0.1",srv.prt); await rd(r)
            m={"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":srv.pai.get()}}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); tok=(await rd(r))["data"]["token"]
            w.close(); await w.wait_closed()
            r,w=await aio.open_connection("127.0.0.1",srv.prt); await rd(r)
            m={"version":"1.0","id":"2","type":"auth","action":"resume","data":{"token":tok}}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); self.assertEqual((await rd(r))["status"],"ok")
            w.close(); await w.wait_closed(); await srv.end()
        aio.run(run())

    def t02(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r,w=await aio.open_connection("127.0.0.1",srv.prt); await rd(r); w.write(b"{bad}\n"); await w.drain(); x=await rd(r); self.assertEqual(x["error"]["code"],"INVALID_JSON"); w.close(); await w.wait_closed(); await srv.end()
        aio.run(run())

    def t03(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r1,w1=await aio.open_connection("127.0.0.1",srv.prt); await rd(r1)
            m={"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":srv.pai.get()}}
            w1.write((js.dumps(m)+"\n").encode()); await w1.drain(); tok=(await rd(r1))["data"]["token"]
            r2,w2=await aio.open_connection("127.0.0.1",srv.prt); await rd(r2)
            m={"version":"1.0","id":"2","type":"auth","action":"resume","data":{"token":tok}}
            w2.write((js.dumps(m)+"\n").encode()); await w2.drain(); self.assertEqual((await rd(r2))["error"]["code"],"HOST_BUSY")
            w1.close(); w2.close(); await w1.wait_closed(); await w2.wait_closed(); await srv.end()
        aio.run(run())

    def t05(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r,w=await aio.open_connection("127.0.0.1",srv.prt); await rd(r)
            m={"version":"1.0","id":"1","type":"auth","action":"resume","data":{"token":"invalid-session-token-123456"}}
            w.write((js.dumps(m)+"\n").encode()); await w.drain(); self.assertEqual((await rd(r))["error"]["code"],"SESSION_EXPIRED")
            w.close(); await w.wait_closed(); await srv.end()
        aio.run(run())

    def t06(self):
        async def run():
            srv=Srv("127.0.0.1",0,0,60,Fak(),log("ERROR")); await srv.sta()
            r1,w1=await aio.open_connection("127.0.0.1",srv.prt); await rd(r1)
            m={"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":srv.pai.get()}}
            w1.write((js.dumps(m)+"\n").encode()); await w1.drain(); tok=(await rd(r1))["data"]["token"]
            w1.close(); await w1.wait_closed(); await aio.sleep(0.02)
            r2,w2=await aio.open_connection("127.0.0.1",srv.prt); await rd(r2)
            m={"version":"1.0","id":"2","type":"auth","action":"resume","data":{"token":tok}}
            w2.write((js.dumps(m)+"\n").encode()); await w2.drain(); self.assertEqual((await rd(r2))["status"],"ok")
            r3,w3=await aio.open_connection("127.0.0.1",srv.prt); await rd(r3)
            m={"version":"1.0","id":"3","type":"auth","action":"resume","data":{"token":tok}}
            w3.write((js.dumps(m)+"\n").encode()); await w3.drain(); self.assertEqual((await rd(r3))["error"]["code"],"HOST_BUSY")
            w2.close(); w3.close(); await w2.wait_closed(); await w3.wait_closed(); await srv.end()
        aio.run(run())

setattr(ST, "test_t01", ST.t01)
setattr(ST, "test_t02", ST.t02)
setattr(ST, "test_t03", ST.t03)
setattr(ST, "test_t04", ST.t04)
setattr(ST, "test_t05", ST.t05)
setattr(ST, "test_t06", ST.t06)
if __name__ == "__main__": uni.main()
