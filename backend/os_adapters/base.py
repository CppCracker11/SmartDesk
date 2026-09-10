from abc import ABC, abstractmethod


class OSAdapter(ABC):
    @abstractmethod
    def mouse_move(self, dx: float, dy: float) -> None: ...

    @abstractmethod
    def mouse_click(self, button: str) -> None: ...

    @abstractmethod
    def mouse_double_click(self) -> None: ...

    @abstractmethod
    def mouse_scroll(self, dx: float, dy: float) -> None: ...

    @abstractmethod
    def key_press(self, key: str) -> None: ...

    @abstractmethod
    def key_release(self, key: str) -> None: ...

    @abstractmethod
    def key_combo(self, keys: list[str]) -> None: ...

    @abstractmethod
    def media_control(self, action: str) -> None: ...

    @abstractmethod
    def presentation_control(self, action: str) -> None: ...
