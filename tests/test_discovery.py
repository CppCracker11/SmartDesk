import asyncio as aio
import unittest as uni
from backend.network.discovery import new

class DT(uni.TestCase):
    def t01(self):
        async def run():
            loop=aio.get_running_loop(); got=[]
            trn=await new(loop,0,lambda:{"type":"SMARTDESK_HOST","port":1234},type("L",(),{"error":lambda *x:None})())
            prt=trn.get_extra_info("sockname")[1]
            class P(aio.DatagramProtocol):
                def mad(self,tr):
                    self.tr=tr; tr.sendto(b"SMARTDESK_DISCOVER",("127.0.0.1",prt))
                def got(self,dat,adr): self.out(dat)
                def out(self,dat): got.append(dat)
            setattr(P,"connection_made",P.mad); setattr(P,"datagram_received",P.got)
            c,_=await loop.create_datagram_endpoint(P,local_addr=("127.0.0.1",0))
            for _ in range(20):
                if got: break
                await aio.sleep(0.01)
            c.close(); trn.close(); self.assertTrue(got); self.assertIn(b"SMARTDESK_HOST",got[0])
        aio.run(run())

setattr(DT,"test_t01",DT.t01)

if __name__ == "__main__": uni.main()
