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

from PySide6.QtCore import Qt, QPoint, Signal, QRect
from PySide6.QtGui import QMouseEvent, QIcon, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QStyleOption, QStylePainter, QStyle

from amcl.ui.theme.core import theme
from amcl.utils.get_resource import r


class TitleBar(QWidget):
    minimize_clicked = Signal()
    close_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start: QPoint | None = None
        self.init_ui()
        self.setFixedHeight(32)
        theme().register(self)

    def init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        self.apply_theme(theme().current())

        self.icon_lab = QLabel()
        self.icon_lab.setFixedSize(30,30)
        self.icon_lab.setScaledContents(True)
        lay.addWidget(self.icon_lab)

        self.title_lab = QLabel("AMCL")
        lay.addWidget(self.title_lab)
        lay.addStretch()

        self.btn_min = QPushButton()
        self.btn_close = QPushButton()
        self.btn_min.setIcon(QIcon(r("assets/img/titlebar/minimize.svg")))
        self.btn_close.setIcon(QIcon(r("assets/img/titlebar/close.svg")))
        
        for btn in (self.btn_min, self.btn_close):
            lay.addWidget(btn)

        self.btn_min.clicked.connect(self.minimize_clicked)
        self.btn_close.clicked.connect(self.close_clicked)

    def apply_theme(self, palette):
        self.setStyleSheet(f"""
             TitleBar{{
                 background:{palette.surface.name(QColor.HexArgb)};
                 border:none;
             }}
             QLabel{{
                 color:{palette.text.name()};
                 font-size:14px;
                 padding-left:6px;
             }}
             QPushButton{{
                 border:none;
                 background:transparent;
                 width:28px;
                 height:28px;
             }}
             QPushButton:hover{{
                 background:{palette.primary.name(QColor.HexArgb)};
                 border-radius:4px;
             }}
         """)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._drag_start = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._drag_start:
            delta = e.globalPosition().toPoint() - self._drag_start
            self.window().move(self.window().pos() + delta)
            self._drag_start = e.globalPosition().toPoint()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        QStylePainter(self).drawPrimitive(QStyle.PE_Widget, opt)