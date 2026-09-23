import asyncio as aio
import time as tim
import unittest as uni

class LT(uni.TestCase):
    def t01(self):
        async def run():
            async def h(r,w):
                dat=await r.readline(); w.write(dat); await w.drain(); w.close(); await w.wait_closed()
            srv=await aio.start_server(h,"127.0.0.1",0); prt=srv.sockets[0].getsockname()[1]
            r,w=await aio.open_connection("127.0.0.1",prt); ts=tim.perf_counter(); w.write(b"ping\n"); await w.drain()
            self.assertEqual(await r.readline(),b"ping\n"); self.assertGreaterEqual((tim.perf_counter()-ts)*1000,0)
            w.close(); await w.wait_closed(); srv.close(); await srv.wait_closed()
        aio.run(run())

setattr(LT, "test_t01", LT.t01)
if __name__ == "__main__": uni.main()
