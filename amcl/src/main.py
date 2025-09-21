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

import sys
from PySide6.QtWidgets import QApplication

from amcl.ui.window.main_window import MainWindow
from amcl.utils.amcl_logger import log
from amcl.utils.config import cfg
from amcl.utils.shutdown_manager import shutdown_mgr


def main():
    app = QApplication(sys.argv)

    log.info("AMCL started")
    cfg.setdefault("log.level", "INFO")

    window = MainWindow()
    window.show()

    def on_shutdown():
        shutdown_mgr.shutdown(timeout=5)

    window.about_to_close.connect(on_shutdown)
    app.aboutToQuit.connect(on_shutdown)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()