from .base import Adp
from .common import kb, ms, key, req, med
import ctypes

class Win(Adp):
    def __init__(self):
        req()
        self.mou = ms.Controller()
        self.key = kb.Controller()

    def mov(self, dx, dy): self.mou.move(dx, dy)
    # Glossary:
    # mov = mouse move
    def clk(self, btn): self.mou.click(getattr(ms.Button, btn), 1)
    # Glossary:
    # clk = click
    # btn = button
    def dbl(self): self.mou.click(ms.Button.left, 2)
    # Glossary:
    # dbl = double click
    def scr(self, dx, dy): self.mou.scroll(dx, dy)
    # Glossary:
    # scr = scroll
    def prs(self, val): self.key.press(key(val))
    # Glossary:
    # prs = press
    def rel(self, val): self.key.release(key(val))
    # Glossary:
    # rel = release
    def cmb(self, ks):
        ps = [key(x) for x in ks]
        try:
            for x in ps: self.key.press(x)
        finally:
            for x in reversed(ps): self.key.release(x)
    # Glossary:
    # cmb = combination
    # ks = keys
    # ps = translated keys
    def med(self, act):
        if act == "volume_up":
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
        elif act == "volume_down":
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
        else:
            x = med()[act]
            self.key.press(x)
            self.key.release(x)
    # Glossary:
    # med = media control
    # act = action
    def pre(self, act): self.prs("RIGHT" if act == "next" else "LEFT")
    # Glossary:
    # pre = presentation control