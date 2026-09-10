import unittest
from backend.protocol.validator import validate_message


class ValidationTests(unittest.TestCase):
    def test_key_validation(self):
        base = {"version": "1.0", "id": "1", "type": "keyboard", "action": "press", "data": {"key": "ENTER"}}
        self.assertTrue(validate_message(base)[0])
        base["data"]["key"] = "NOT_A_KEY"
        self.assertFalse(validate_message(base)[0])

    def test_pair_code_validation(self):
        msg = {"version": "1.0", "id": "1", "type": "auth", "action": "pair", "data": {"code": "123456"}}
        self.assertTrue(validate_message(msg)[0])
        msg["data"]["code"] = "123"
        self.assertFalse(validate_message(msg)[0])


if __name__ == "__main__":
    unittest.main()
