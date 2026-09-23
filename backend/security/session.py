import secrets as sec
import time as tim

class Ses:
    def __init__(self, tmo=3600):
        self.tok = None
        self.ts = 0.0
        self.tmo = tmo
        self.act = False
        self.cid = None

    def new(self, cid):
        self.tok = sec.token_urlsafe(32)
        self.ts = tim.monotonic()
        self.act = True
        self.cid = cid
        return self.tok
    # Glossary:
    # new = create session
    # cid = connection id

    def ok(self, tok):
        if not self.tok or not tok:
            return False
        if tim.monotonic() - self.ts >= self.tmo:
            self.clr()
            return False
        return sec.compare_digest(self.tok, tok)
    # Glossary:
    # ok = token validity
    # tok = token

    def has(self):
        return self.ok(self.tok)
    # Glossary:
    # has = valid session exists

    def use(self, tok, cid):
        if not self.ok(tok) or self.act:
            return False
        self.act = True
        self.cid = cid
        return True
    # Glossary:
    # use = activate session connection
    # cid = connection id

    def rel(self, tok, cid):
        if self.ok(tok) and self.cid == cid:
            self.act = False
            self.cid = None
            return True
        return False
    # Glossary:
    # rel = release connection
    # cid = connection id

    def clr(self):
        self.tok = None
        self.ts = 0.0
        self.act = False
        self.cid = None
    # Glossary:
    # clr = clear session
