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