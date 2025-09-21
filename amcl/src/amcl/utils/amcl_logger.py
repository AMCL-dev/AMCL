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

import logging, sys
from datetime import datetime, timezone
from pathlib import Path
import inspect
import os

from PySide6.QtCore import QObject, QTimer, QMutex, QMutexLocker

from amcl.utils.shutdown_manager import shutdown_mgr

__all__ = ["log"]

_JSON_PATH = Path.home() / ".amcl" / "logs"
_FMT = "%(asctime)s | %(levelname)-8s | %(threadName)-16s | %(filename)s:%(lineno)d | %(message)s"
_FORMATTER = logging.Formatter(_FMT, datefmt="%Y-%m-%d %H:%M:%S")


class _AMCLLogger(QObject):
    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.file = None
        self.path = None
        self.flush_timer = QTimer()
        self.flush_timer.timeout.connect(self._flush)
        self.flush_timer.start(100)

    def _get_path(self):
        _JSON_PATH.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now(tz=timezone.utc).astimezone().strftime("%Y%m%d")
        return _JSON_PATH / f"launcher_log_{date_str}.log"

    def _should_rotate(self):
        if not self.path:
            return True
        current_date = datetime.now(tz=timezone.utc).astimezone().strftime("%Y%m%d")
        return self.path.name != f"launcher_log_{current_date}.log"

    def _flush(self):
        # ensure the log file is flushed to disk
        if self.file:
            try:
                self.file.flush()
                os.fsync(self.file.fileno())
            except:
                pass

    def _get_caller_info(self):
        try:
            stack = inspect.stack()
            for frame in stack[3:]:  # skip the first 3 frames (current method, log method, and caller)
                filename = frame.filename
                if 'amcl_logger' not in filename and 'logging' not in filename:
                    return os.path.basename(filename), frame.lineno
        except:
            pass
        return "unknown", 0

    def log(self, level, msg, *args, **kwargs):
        filename, lineno = self._get_caller_info()

        record = logging.LogRecord(
            name="AMCL",
            level=level,
            pathname=filename,
            lineno=lineno,
            msg=msg,
            args=args,
            exc_info=kwargs.get("exc_info"),
            func=None,
        )

        formatted_msg = _FORMATTER.format(record)
        print(formatted_msg, flush=True)

        try:
            if self._should_rotate():
                if self.file:
                    self.file.close()
                self.path = self._get_path()
                self.file = self.path.open("a", encoding="utf-8")

            if self.file:
                self.file.write(formatted_msg + "\n")
                self._flush()

        except Exception as e:
            print(f"Log file error: {e}", file=sys.stderr, flush=True)

    def shutdown(self):
        self.flush_timer.stop()
        if self.file:
            self.file.close()
            self.file = None

_logger = _AMCLLogger()

class LogInterface:
    def debug(self, msg, *args, **kwargs):
        _logger.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        _logger.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        _logger.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        _logger.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        _logger.log(logging.CRITICAL, msg, *args, **kwargs)

    def shutdown(self):
        _logger.shutdown()


log = LogInterface()
shutdown_mgr.add(log.shutdown)