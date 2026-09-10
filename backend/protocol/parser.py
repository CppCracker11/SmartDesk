from .messages import decode_message


class ProtocolParser:
    def __init__(self, max_line: int = 65536):
        self.buffer = bytearray()
        self.max_line = max_line

    def feed(self, data: bytes) -> list[dict]:
        self.buffer.extend(data)
        if len(self.buffer) > self.max_line:
            raise ValueError("Message buffer exceeded limit")

        messages = []
        while b"\n" in self.buffer:
            index = self.buffer.index(b"\n")
            line = bytes(self.buffer[:index]).strip()
            del self.buffer[:index + 1]
            if not line:
                continue
            messages.append(decode_message(line))
        return messages
