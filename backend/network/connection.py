import asyncio
import time

from ..protocol.messages import encode_message, error_response, ok_response
from ..protocol.validator import validate_message


class ClientConnection:
    def __init__(self, reader, writer, pairing, session, dispatcher, host_info, logger):
        self.reader = reader
        self.writer = writer
        self.pairing = pairing
        self.session = session
        self.dispatcher = dispatcher
        self.host_info = host_info
        self.logger = logger
        self.authenticated = False
        self.parser_buffer = bytearray()

    async def send(self, message):
        self.writer.write(encode_message(message))
        await self.writer.drain()

    async def run(self):
        peer = self.writer.get_extra_info("peername")
        self.logger.info("Client connected: %s", peer[0] if peer else "unknown")
        self.writer.write(encode_message({"type": "state", "state": "AUTHENTICATING"}))
        await self.writer.drain()

        try:
            while True:
                data = await self.reader.read(4096)
                if not data:
                    break
                self.parser_buffer.extend(data)
                if len(self.parser_buffer) > 65536:
                    await self.send(error_response("", "MESSAGE_TOO_LARGE", "Message is too large"))
                    break

                while b"\n" in self.parser_buffer:
                    index = self.parser_buffer.index(b"\n")
                    line = bytes(self.parser_buffer[:index]).strip()
                    del self.parser_buffer[:index + 1]
                    if not line:
                        continue
                    await self.handle_line(line)
        except (ConnectionError, TimeoutError, asyncio.CancelledError):
            pass
        except Exception as exc:
            self.logger.error("Client handling error: %s", exc)
        finally:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except Exception:
                pass
            self.logger.info("Client disconnected")

    async def handle_line(self, line: bytes):
        import json
        try:
            message = json.loads(line.decode("utf-8"))
            if not isinstance(message, dict):
                raise ValueError
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            await self.send(error_response("", "INVALID_JSON", "Invalid SmartDesk message"))
            return

        valid, code, text = validate_message(message)
        msg_id = message.get("id", "")
        if not valid:
            await self.send(error_response(msg_id, code, text))
            return

        msg_type = message["type"]
        action = message["action"]
        if not self.authenticated:
            if msg_type != "auth":
                await self.send(error_response(msg_id, "UNAUTHORIZED", "Pair the controller before sending commands"))
                return
            if action == "pair":
                if not self.pairing.verify(message["data"]["code"]):
                    await self.send(error_response(msg_id, "PAIRING_FAILED", "Pairing failed"))
                    return
                token = self.session.create()
                self.authenticated = True
                self.logger.info("Pairing successful")
                await self.send(ok_response(msg_id, {"token": token, "state": "AUTHENTICATED"}))
                return
            if action == "resume":
                token = message["data"]["token"]
                if not self.session.valid(token):
                    await self.send(error_response(msg_id, "RESUME_FAILED", "Session token is invalid or expired"))
                    return
                self.authenticated = True
                await self.send(ok_response(msg_id, {"token": token, "state": "AUTHENTICATED"}))
                return

        if message.get("token") is None or not self.session.valid(message.get("token")):
            await self.send(error_response(msg_id, "UNAUTHORIZED", "Invalid session token"))
            return

        if msg_type == "system":
            if action == "ping":
                now = time.time_ns()
                await self.send(ok_response(msg_id, {"pong_ns": now}))
            elif action == "get_host_info":
                await self.send(ok_response(msg_id, self.host_info))
            elif action == "disconnect":
                await self.send(ok_response(msg_id))
                self.writer.close()
            return

        response = self.dispatcher.dispatch(message)
        await self.send(response)
