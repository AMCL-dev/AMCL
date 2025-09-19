# harmony_widget_base.py
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QPaintEvent
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


class HarmonyWidgetBase(QWidget):
    """鸿蒙风格基础组件类"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._radius = 12
        self._shadow_enabled = True
        self._shadow_color = QColor(0, 0, 0, 25)
        self._shadow_blur = 12
        self._shadow_offset = (0, 4)
        self._background_color = QColor("#FFFFFF")
        self._border_color = QColor("#E6E8EB")
        self._border_width = 1

        self._setup_shadow()
        self._setup_animations()

    def _setup_shadow(self):
        """设置阴影效果"""
        if self._shadow_enabled:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(self._shadow_blur)
            shadow.setColor(self._shadow_color)
            shadow.setOffset(*self._shadow_offset)
            self.setGraphicsEffect(shadow)

    def _setup_animations(self):
        """设置动画"""
        self._bg_animation = QPropertyAnimation(self, b"background_color")
        self._bg_animation.setDuration(200)
        self._bg_animation.setEasingCurve(QEasingCurve.OutCubic)

        self._border_animation = QPropertyAnimation(self, b"border_color")
        self._border_animation.setDuration(200)
        self._border_animation.setEasingCurve(QEasingCurve.OutCubic)

    @Property(QColor)
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, color):
        self._background_color = color
        self.update()

    @Property(QColor)
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, color):
        self._border_color = color
        self.update()

    def paintEvent(self, event: QPaintEvent):
        """自定义绘制"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        painter.setBrush(QBrush(self._background_color))
        painter.setPen(QPen(self._border_color, self._border_width))

        rect = self.rect()
        painter.drawRoundedRect(rect, self._radius, self._radius)