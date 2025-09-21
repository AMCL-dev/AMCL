import json, os
from pathlib import Path
from typing import Any, Dict, Optional

from PySide6.QtCore import QObject, QTimer, QMutex, QMutexLocker, QThread

from amcl.utils.shutdown_manager import shutdown_mgr

_JSON_PATH = Path.home() / ".amcl" / "config" / "amcl.json"
_DEBOUNCE_MS = 300


class ConfigWorker(QObject):
    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path
        self.data = {}
        self.mutex = QMutex()
        self.shutting_down = False
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.dump)

    def ensure_file(self):
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.json_path.exists():
            self.json_path.write_text("{}", encoding="utf-8")

    def load(self):
        with QMutexLocker(self.mutex):
            self.ensure_file()
            try:
                with self.json_path.open("r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def dump(self):
        with QMutexLocker(self.mutex):
            if self.shutting_down:
                return
            try:
                with self.json_path.open("w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
            except Exception:
                pass

    def trigger_save(self):
        if not self.shutting_down:
            self.save_timer.stop()
            self.save_timer.start(_DEBOUNCE_MS)

    def prepare_shutdown(self):
        with QMutexLocker(self.mutex):
            self.shutting_down = True
            self.save_timer.stop()


class _Config(Dict[str, Any]):
    _instance: Optional["_Config"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._worker = ConfigWorker(_JSON_PATH)
            cls._instance._worker.load()
        return cls._instance

    def reload(self):
        self._worker.load()

    def save(self):
        self._worker.dump()

    def shutdown(self) -> None:
        self._worker.prepare_shutdown()
        self._worker.dump()

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)
        self._worker.data[key] = value
        self._worker.trigger_save()

    def setdefault(self, key: str, default: Any) -> Any:
        if key not in self:
            self[key] = default
        return self[key]

    def __getitem__(self, key):
        return self._worker.data.get(key, super().get(key, None))

    def get(self, key, default=None):
        return self._worker.data.get(key, default)

    @property
    def log_level(self) -> str:
        return self.get("log.level", "INFO").upper()

    @log_level.setter
    def log_level(self, lvl: str) -> None:
        self["log.level"] = lvl.upper()


cfg: _Config = _Config()
shutdown_mgr.add(cfg.shutdown)