import unittest
from backend.security.pairing import PairingManager
from backend.security.session import SessionManager


class SecurityTests(unittest.TestCase):
    def test_pairing_one_time(self):
        p = PairingManager(60)
        code = p.get_code()
        self.assertTrue(p.verify(code))
        self.assertFalse(p.verify(code))

    def test_wrong_pairing_code(self):
        p = PairingManager(60)
        self.assertFalse(p.verify("000000"))

    def test_session_token(self):
        s = SessionManager(60)
        token = s.create()
        self.assertTrue(s.valid(token))
        self.assertFalse(s.valid("bad"))


if __name__ == "__main__":
    unittest.main()
