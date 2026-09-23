import unittest as uni
from backend.commands.dispatcher import Cmd

class Fak:
    def __init__(self): self.cal=[]
    def mov(self,x,y): self.cal.append(("mov",x,y))
    def clk(self,x): self.cal.append(("clk",x))
    def dbl(self): self.cal.append(("dbl",))
    def scr(self,x,y): self.cal.append(("scr",x,y))
    def prs(self,x): self.cal.append(("prs",x))
    def rel(self,x): self.cal.append(("rel",x))
    def cmb(self,x): self.cal.append(("cmb",x))
    def med(self,x): self.cal.append(("med",x))
    def pre(self,x): self.cal.append(("pre",x))

class DT(uni.TestCase):
    def t01(self):
        a=Fak(); l=type("L",(),{"info":lambda *x:None,"error":lambda *x:None})(); c=Cmd(a,l)
        r=c.run({"id":"1","type":"mouse","action":"move","data":{"dx":3,"dy":4}})
        self.assertEqual(r["status"],"ok"); self.assertEqual(a.cal,[("mov",3,4)])

    def t02(self):
        a=Fak(); l=type("L",(),{"info":lambda *x:None,"error":lambda *x:None})(); c=Cmd(a,l)
        r=c.run({"id":"1","type":"keyboard","action":"combo","data":{"keys":["CTRL","c"]}})
        self.assertEqual(r["status"],"ok"); self.assertEqual(a.cal,[("cmb",["CTRL","c"])])

setattr(DT, "test_t01", DT.t01)
setattr(DT, "test_t02", DT.t02)
if __name__ == "__main__": uni.main()
