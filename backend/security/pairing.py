import secrets
import time


class PairingManager:
    def __init__(self, timeout: int):
        self.timeout = timeout
        self.code = self._new_code()
        self.created = time.monotonic()
        self.used = False

    def _new_code(self) -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    def get_code(self) -> str:
        if time.monotonic() - self.created >= self.timeout or self.used:
            self.code = self._new_code()
            self.created = time.monotonic()
            self.used = False
        return self.code

    def verify(self, code: str) -> bool:
        if self.used or time.monotonic() - self.created >= self.timeout:
            return False
        if secrets.compare_digest(code, self.code):
            self.used = True
            return True
        return False
