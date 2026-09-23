import unittest as uni
from backend.protocol.messages import enc
from backend.protocol.parser import Pro
from backend.protocol.validator import val

class PT(uni.TestCase):
    def t01(self):
        p = Pro(); raw = enc({"a":1}) + enc({"b":2})
        self.assertEqual(p.fed(raw[:5]), [])
        self.assertEqual(p.fed(raw[5:]), [{"a":1},{"b":2}])

    def t02(self):
        m = {"version":"1.0","id":"1","type":"mouse","action":"move","data":{"dx":2,"dy":-1}}
        self.assertTrue(val(m)[0])

    def t03(self):
        m = {"version":"1.0","id":"1","type":"mouse","action":"bad","data":{}}
        self.assertFalse(val(m)[0]); self.assertEqual(val(m)[1], "INVALID_COMMAND")

    def t04(self):
        p = Pro()
        with self.assertRaises(ValueError): p.fed(b"{bad}\n")

    def t05(self):
        m = {"version":"1.0","id":"1","type":"keyboard","action":"combo","data":{"keys":["CTRL","c"]}}
        self.assertTrue(val(m)[0])

setattr(PT, "test_t01", PT.t01)
setattr(PT, "test_t02", PT.t02)
setattr(PT, "test_t03", PT.t03)
setattr(PT, "test_t04", PT.t04)
setattr(PT, "test_t05", PT.t05)
if __name__ == "__main__": uni.main()
