import sys, random, os, signal, ctypes, platform
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QComboBox,
                               QPushButton, QSpacerItem, QSizePolicy, QApplication)


def _hard_kill():
    os.kill(os.getpid(), signal.SIGSEGV)


def _zero_div():
    _ = 1 / 0


def _stack_bomb():
    ctypes.pythonapi.PyRun_SimpleString(b'import ctypes\nctypes.CFUNCTYPE(None)(id)')


def _segfault():
    ctypes.memmove(0, 1, 1)
    _hard_kill()


class DevWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevWindow")
        self.resize(300, 120)
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        sys.excepthook = lambda *a: _hard_kill()

        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(_hard_kill)

        self.combo = QComboBox()
        self.combo.addItems(["随机", "除以 0", "sys.exit(-1)",
                             "段错误 (ctypes)", "递归爆栈"])
        self.btn = QPushButton("执行崩溃")
        self.btn.clicked.connect(self._crash)

        lay = QVBoxLayout(self)
        lay.addWidget(self.combo)
        lay.addWidget(self.btn)
        lay.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def _crash(self):
        mode = self.combo.currentText()
        if mode == "随机":
            mode = random.choice(["除以 0", "sys.exit(-1)",
                                  "段错误 (ctypes)", "递归爆栈"])

        if mode == "除以 0":
            _zero_div()
        elif mode == "sys.exit(-1)":
            sys.exit(-1)
        elif mode == "段错误 (ctypes)":
            _segfault()
        elif mode == "递归爆栈":
            _stack_bomb()