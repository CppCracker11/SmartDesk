import unittest as uni
from backend.os_adapters.common import MAP

class AT(uni.TestCase):
    def t01(self):
        self.assertEqual(MAP["CTRL"], "ctrl")
        self.assertEqual(MAP["CMD"], "cmd")
        self.assertNotEqual(MAP["CTRL"], MAP["CMD"])

setattr(AT, "test_t01", AT.t01)
if __name__ == "__main__": uni.main()
