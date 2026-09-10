import unittest

from backend.protocol.messages import encode_message
from backend.protocol.parser import ProtocolParser
from backend.protocol.validator import validate_message


class ProtocolTests(unittest.TestCase):
    def test_framing_handles_multiple_messages(self):
        parser = ProtocolParser()
        raw = encode_message({"a": 1}) + encode_message({"b": 2})
        self.assertEqual(parser.feed(raw[:5]), [])
        self.assertEqual(parser.feed(raw[5:]), [{"a": 1}, {"b": 2}])

    def test_valid_command(self):
        message = {"version": "1.0", "id": "1", "type": "mouse", "action": "move", "data": {"dx": 2, "dy": -1}}
        self.assertTrue(validate_message(message)[0])

    def test_invalid_command(self):
        message = {"version": "1.0", "id": "1", "type": "mouse", "action": "explode", "data": {}}
        self.assertFalse(validate_message(message)[0])

    def test_invalid_data(self):
        message = {"version": "1.0", "id": "1", "type": "mouse", "action": "move", "data": {"dx": "bad", "dy": 1}}
        self.assertFalse(validate_message(message)[0])

    def test_malformed_json_is_rejected(self):
        parser = ProtocolParser()
        with self.assertRaises(ValueError):
            parser.feed(b"{not json}\n")


if __name__ == "__main__":
    unittest.main()
