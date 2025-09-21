"""
Astra Minecraft Launcher

Copyright (C) 2025 hmr-BH <1218271192@qq.com> and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the Eclipse Public License, Version 2.0 (EPL-2.0),
as published by the Eclipse Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Eclipse Public License 2.0 for more details.

You should have received a copy of the Eclipse Public License 2.0
along with this program.  For the full text of the Eclipse Public License 2.0,
see <https://www.eclipse.org/legal/epl-2.0/>.
"""

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