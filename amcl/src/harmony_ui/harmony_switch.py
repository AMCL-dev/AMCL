# harmony_switch.py
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QMouseEvent
from PySide6.QtWidgets import QWidget
from harmony_theme import HarmonyTheme


class HarmonySwitch(QWidget):
    """鸿蒙风格开关组件"""

    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 状态属性
        self._is_checked = False
        self._is_hovered = False
        self._is_pressed = False
        self._is_enabled = True

        # 尺寸配置
        self._track_width = 44
        self._track_height = 24
        self._thumb_size = 20
        self._thumb_margin = 2

        # 颜色配置
        self._track_off_color = QColor("#E5E7EB")
        self._track_on_color = QColor(HarmonyTheme.PrimaryColor)
        self._track_disabled_color = QColor("#F3F4F6")

        self._thumb_off_color = QColor("#FFFFFF")
        self._thumb_on_color = QColor("#FFFFFF")
        self._thumb_disabled_color = QColor("#D1D5DB")

        # 动画
        self._thumb_animation = QPropertyAnimation(self, b"thumb_position")
        self._thumb_animation.setDuration(200)
        self._thumb_animation.setEasingCurve(QEasingCurve.OutCubic)

        self._thumb_position = 0
        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedSize(self._track_width, self._track_height)
        self.setCursor(Qt.PointingHandCursor)

    def thumb_position(self):
        return getattr(self, '_thumb_position', 0)

    def set_thumb_position(self, position):
        self._thumb_position = position
        self.update()
        
    thumb_position = Property(float, thumb_position, set_thumb_position)

    def paintEvent(self, event):
        """绘制开关"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制轨道
        self._draw_track(painter)

        # 绘制滑块
        self._draw_thumb(painter)

    def _draw_track(self, painter: QPainter):
        """绘制轨道"""
        track_rect = QRect(0, 0, self._track_width, self._track_height)

        if not self._is_enabled:
            color = self._track_disabled_color
        elif self._is_checked:
            color = self._track_on_color
        else:
            color = self._track_off_color

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(track_rect, self._track_height // 2, self._track_height // 2)

    def _draw_thumb(self, painter: QPainter):
        """绘制滑块"""
        thumb_x = int(self._thumb_position)
        thumb_y = self._thumb_margin
        thumb_rect = QRect(thumb_x, thumb_y, self._thumb_size, self._thumb_size)

        if not self._is_enabled:
            color = self._thumb_disabled_color
        else:
            color = self._thumb_on_color if self._is_checked else self._thumb_off_color

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(thumb_rect)

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下"""
        if event.button() == Qt.LeftButton and self._is_enabled:
            self._is_pressed = True
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放"""
        if event.button() == Qt.LeftButton and self._is_pressed:
            self._is_pressed = False
            if self.rect().contains(event.pos()):
                self.toggle()

    def enterEvent(self, event):
        """鼠标进入"""
        self._is_hovered = True
        self.update()

    def leaveEvent(self, event):
        """鼠标离开"""
        self._is_hovered = False
        self.update()

    def toggle(self):
        """切换状态"""
        self.set_checked(not self._is_checked)

    def set_checked(self, checked: bool):
        """设置状态"""
        if self._is_checked != checked:
            self._is_checked = checked
            self._animate_thumb()
            self.toggled.emit(self._is_checked)

    def _animate_thumb(self):
        """动画滑块"""
        start_pos = 0 if not self._is_checked else self._track_width - self._thumb_size - self._thumb_margin * 2
        end_pos = self._track_width - self._thumb_size - self._thumb_margin * 2 if self._is_checked else 0

        self._thumb_animation.setStartValue(start_pos)
        self._thumb_animation.setEndValue(end_pos)
        self._thumb_animation.start()

    def is_checked(self):
        return self._is_checked

    def set_enabled(self, enabled: bool):
        """设置启用状态"""
        self._is_enabled = enabled
        self.setCursor(Qt.PointingHandCursor if enabled else Qt.ForbiddenCursor)
        self.update()