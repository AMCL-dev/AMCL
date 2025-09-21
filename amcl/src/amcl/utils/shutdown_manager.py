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