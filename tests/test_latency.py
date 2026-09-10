import asyncio
import time
import unittest


class LatencyTests(unittest.TestCase):
    def test_loopback_latency_measurement(self):
        async def run():
            async def handler(reader, writer):
                data = await reader.readline()
                writer.write(data)
                await writer.drain()
                writer.close()
                await writer.wait_closed()

            server = await asyncio.start_server(handler, "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            started = time.perf_counter()
            writer.write(b"ping\n")
            await writer.drain()
            self.assertEqual(await reader.readline(), b"ping\n")
            elapsed = (time.perf_counter() - started) * 1000
            writer.close()
            await writer.wait_closed()
            server.close()
            await server.wait_closed()
            self.assertGreaterEqual(elapsed, 0)

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
