from typing import Protocol
from PySide6.QtCore import QObject, Signal
from .palettes import BluePalette, DarkBluePalette

class ThemeClient(Protocol):
    def apply_theme(self, palette): ...

class ThemeManager(QObject):
    theme_changed = Signal(object)

    _instance = None

    def __new__(cls, *a, **k):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._current = BluePalette     # 默认主题
        self._clients: list[ThemeClient] = []

    # public function
    def current(self):
        return self._current

    def switch(self, palette_cls):
        self._current = palette_cls
        self.theme_changed.emit(palette_cls)
        self._repolish()

    def register(self, client: ThemeClient):
        self._clients.append(client)
        client.apply_theme(self._current)

    def _repolish(self):
        for c in self._clients:
            c.apply_theme(self._current)

_THEME = ThemeManager()   # global singleton

def theme() -> ThemeManager:
    return _THEME