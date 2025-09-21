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
from PIL.ImageQt import QPixmap
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from amcl.ui.components.titlebar import TitleBar
from amcl.ui.utils.frameless_helper import FramelessHelper
from amcl.utils.amcl_logger import log
from amcl.utils.get_resource import r


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

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.logo_label = QLabel()
        logo_path = r("assets/img/logo/logo-256x.png")
        self.logo_pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setScaledContents(True)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.logo_label, 0, Qt.AlignCenter)
        self.main_layout.addStretch()


    def closeEvent(self, event):
        log.info("MainWindow closeEvent called, AMCL is shutting down")
        event.accept()  # hide the window first
        # put the real shutdown into the next event loop, to prevent blocking GUI
        self.about_to_close.emit()