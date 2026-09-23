from .messages import dec
import json as js


class Pro:
    def __init__(self, lim=65536):
        self.buf = bytearray()
        self.lim = lim

    def fed(self, dat):
        self.buf.extend(dat)
        if len(self.buf) > self.lim:
            raise ValueError("message buffer exceeded limit")
        out = []
        while b"\n" in self.buf:
            idx = self.buf.index(b"\n")
            lin = bytes(self.buf[:idx]).strip()
            del self.buf[:idx + 1]
            if not lin:
                continue
            try:
                out.append(dec(lin))
            except (js.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
                raise ValueError("invalid json") from exc
        return out
# Glossary:
# Pro = protocol parser
# fed = feed bytes
# buf = buffer
# lim = limit
# dat = data
# out = output
# idx = index
# lin = line
