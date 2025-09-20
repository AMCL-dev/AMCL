from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QMainWindow, QTextEdit
from amcl.ui.components.titlebar import TitleBar
from amcl.ui.utils.frameless_helper import FramelessHelper
from amcl.ui.window.dev_window import DevWindow


class MainWindow(QMainWindow):
    _margin = 6  # resize border width

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AMCL")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(900, 580)

        self._drag_pos: QPoint | None = None
        self._drag_rect: QRect | None = None

        self.title_bar = TitleBar(self)
        self.setMenuWidget(self.title_bar)

        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.close_clicked.connect(self.close)

        self.frameless_helper = FramelessHelper(self, border=6)

        self.dev = DevWindow()
        self.dev.show()