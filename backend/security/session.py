import secrets
import time


class SessionManager:
    def __init__(self, timeout: int = 3600):
        self.token = None
        self.created = 0.0
        self.timeout = timeout

    def create(self) -> str:
        self.token = secrets.token_urlsafe(32)
        self.created = time.monotonic()
        return self.token

    def valid(self, token: str | None) -> bool:
        if not self.token or not token:
            return False
        if time.monotonic() - self.created >= self.timeout:
            self.clear()
            return False
        return secrets.compare_digest(self.token, token)

    def clear(self) -> None:
        self.token = None
        self.created = 0.0
