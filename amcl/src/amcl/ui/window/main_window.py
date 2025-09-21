from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow
from amcl.ui.components.titlebar import TitleBar
from amcl.ui.utils.frameless_helper import FramelessHelper
from amcl.utils.amcl_logger import log


class MainWindow(QMainWindow):
    about_to_close = Signal()

    def __init__(self):
        super().__init__()

        log.info("MainWindow created")

        self.setWindowTitle("AMCL")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(900, 580)

        self.title_bar = TitleBar(self)
        self.setMenuWidget(self.title_bar)

        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.close_clicked.connect(self.close)

        self.frameless_helper = FramelessHelper(self, border=4)

    def closeEvent(self, event):
        log.info("MainWindow closeEvent called, AMCL is shutting down")
        event.accept()  # hide the window first
        # put the real shutdown into the next event loop, to prevent blocking GUI
        self.about_to_close.emit()