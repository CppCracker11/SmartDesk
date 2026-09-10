import asyncio
import json
import unittest

from backend.network.server import SmartDeskServer
from backend.utils.logging import setup_logging


class FakeAdapter:
    def mouse_move(self, dx, dy): pass
    def mouse_click(self, button): pass
    def mouse_double_click(self): pass
    def mouse_scroll(self, dx, dy): pass
    def key_press(self, key): pass
    def key_release(self, key): pass
    def key_combo(self, keys): pass
    def media_control(self, action): pass
    def presentation_control(self, action): pass


async def read_message(reader):
    return json.loads((await reader.readline()).decode())


class ServerTests(unittest.TestCase):
    def test_pair_ping_and_resume(self):
        async def run():
            logger = setup_logging("ERROR")
            server = SmartDeskServer("127.0.0.1", 0, 0, 60, FakeAdapter(), logger)
            await server.start()
            port = server.port

            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            state = await read_message(reader)
            self.assertEqual(state["state"], "AUTHENTICATING")

            pair = {"version": "1.0", "id": "1", "type": "auth", "action": "pair", "data": {"code": server.pairing.get_code()}}
            writer.write((json.dumps(pair) + "\n").encode())
            await writer.drain()
            response = await read_message(reader)
            self.assertEqual(response["status"], "ok")
            token = response["data"]["token"]
            writer.close()
            await writer.wait_closed()

            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            await read_message(reader)
            resume = {"version": "1.0", "id": "2", "type": "auth", "action": "resume", "data": {"token": token}}
            writer.write((json.dumps(resume) + "\n").encode())
            await writer.drain()
            response = await read_message(reader)
            self.assertEqual(response["status"], "ok")

            ping = {"version": "1.0", "id": "3", "type": "system", "action": "ping", "data": {}, "token": token}
            writer.write((json.dumps(ping) + "\n").encode())
            await writer.drain()
            response = await read_message(reader)
            self.assertEqual(response["status"], "ok")
            self.assertIn("pong_ns", response["data"])

            writer.close()
            await writer.wait_closed()
            await server.stop()

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
