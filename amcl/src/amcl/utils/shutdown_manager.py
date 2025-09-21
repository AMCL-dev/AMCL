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

from typing import Callable, List
from PySide6.QtCore import QObject, QMutex, QMutexLocker

class _Mgr(QObject):
    def __init__(self) -> None:
        super().__init__()
        self._tasks: List[Callable] = []
        self._mutex = QMutex()
        self._shutting_down = False

    def add(self, callback: Callable) -> None:
        with QMutexLocker(self._mutex):
            self._tasks.append(callback)

    def shutdown(self, timeout: float = 3.0) -> None:
        with QMutexLocker(self._mutex):
            if self._shutting_down:
                return
            self._shutting_down = True

            # execute all shutdown tasks
            for callback in self._tasks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error during shutdown: {e}")

            self._tasks.clear()


shutdown_mgr: _Mgr = _Mgr()