import secrets as sec
import time as tim

class Pai:
    def __init__(self, tmo):
        self.tmo = tmo
        self.cod = self.new()
        self.ts = tim.monotonic()
        self.use = False

    def new(self):
        return f"{sec.randbelow(1000000):06d}"
    # Glossary:
    # new = new pairing code

    def get(self):
        if tim.monotonic() - self.ts >= self.tmo or self.use:
            self.cod = self.new()
            self.ts = tim.monotonic()
            self.use = False
        return self.cod
    # Glossary:
    # get = get active code

    def ver(self, cod):
        if self.use or tim.monotonic() - self.ts >= self.tmo:
            return False
        if sec.compare_digest(cod, self.cod):
            self.use = True
            return True
        return False
    # Glossary:
    # ver = verify code
    # cod = code
