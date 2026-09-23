from abc import ABC, abstractmethod

class Adp(ABC):
    @abstractmethod
    def mov(self, dx, dy): ...
    # Glossary:
    # mov = mouse move
    @abstractmethod
    def clk(self, btn): ...
    # Glossary:
    # clk = mouse click
    # btn = button
    @abstractmethod
    def dbl(self): ...
    # Glossary:
    # dbl = double click
    @abstractmethod
    def scr(self, dx, dy): ...
    # Glossary:
    # scr = scroll
    @abstractmethod
    def prs(self, key): ...
    # Glossary:
    # prs = key press
    @abstractmethod
    def rel(self, key): ...
    # Glossary:
    # rel = key release
    @abstractmethod
    def cmb(self, keys): ...
    # Glossary:
    # cmb = key combination
    @abstractmethod
    def med(self, act): ...
    # Glossary:
    # med = media control
    # act = action
    @abstractmethod
    def pre(self, act): ...
    # Glossary:
    # pre = presentation control

class Nul(Adp):
    def mov(self, dx, dy): raise RuntimeError("input backend unavailable")
    # Glossary:
    # mov = mouse move
    def clk(self, btn): raise RuntimeError("input backend unavailable")
    # Glossary:
    # clk = mouse click
    def dbl(self): raise RuntimeError("input backend unavailable")
    # Glossary:
    # dbl = double click
    def scr(self, dx, dy): raise RuntimeError("input backend unavailable")
    # Glossary:
    # scr = scroll
    def prs(self, key): raise RuntimeError("input backend unavailable")
    # Glossary:
    # prs = key press
    def rel(self, key): raise RuntimeError("input backend unavailable")
    # Glossary:
    # rel = key release
    def cmb(self, keys): raise RuntimeError("input backend unavailable")
    # Glossary:
    # cmb = key combination
    def med(self, act): raise RuntimeError("input backend unavailable")
    # Glossary:
    # med = media control
    def pre(self, act): raise RuntimeError("input backend unavailable")
    # Glossary:
    # pre = presentation control
