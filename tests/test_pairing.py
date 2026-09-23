import unittest as uni
from backend.security.pairing import Pai
from backend.security.session import Ses

class ST(uni.TestCase):
    def t01(self):
        p = Pai(60); c = p.get(); self.assertTrue(p.ver(c)); self.assertFalse(p.ver(c))

    def t02(self):
        p = Pai(60); self.assertFalse(p.ver("000000"))

    def t03(self):
        s = Ses(60); t = s.new(1); self.assertTrue(s.ok(t)); self.assertTrue(s.has()); self.assertTrue(s.act); self.assertFalse(s.ok("bad"))

    def t04(self):
        s = Ses(60); t = s.new(1); self.assertTrue(s.rel(t, 1)); self.assertTrue(s.ok(t)); self.assertFalse(s.act); self.assertTrue(s.use(t, 2)); self.assertTrue(s.act)

    def t05(self):
        s = Ses(60); t = s.new(1); self.assertFalse(s.rel(t, 2)); self.assertTrue(s.act); self.assertTrue(s.ok(t))

    def t06(self):
        s = Ses(1); t = s.new(1); s.ts -= 2; self.assertFalse(s.ok(t)); self.assertFalse(s.has()); self.assertIsNone(s.tok)

setattr(ST, "test_t01", ST.t01)
setattr(ST, "test_t02", ST.t02)
setattr(ST, "test_t03", ST.t03)
setattr(ST, "test_t04", ST.t04)
setattr(ST, "test_t05", ST.t05)
setattr(ST, "test_t06", ST.t06)
if __name__ == "__main__": uni.main()
