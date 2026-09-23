import unittest as uni
from backend.protocol.validator import val

class VT(uni.TestCase):
    def t01(self):
        m={"version":"1.0","id":"1","type":"keyboard","action":"press","data":{"key":"ENTER"}}
        self.assertTrue(val(m)[0]); m["data"]["key"]="BAD"; self.assertFalse(val(m)[0])

    def t02(self):
        m={"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":"123456"}}
        self.assertTrue(val(m)[0]); m["data"]["code"]="123"; self.assertFalse(val(m)[0])

    def t03(self):
        m={"version":"1.0","id":"1","type":"mouse","action":"move","data":{"dx":"x","dy":1}}
        self.assertEqual(val(m)[1], "INVALID_PARAMETER")

setattr(VT, "test_t01", VT.t01)
setattr(VT, "test_t02", VT.t02)
setattr(VT, "test_t03", VT.t03)
if __name__ == "__main__": uni.main()

