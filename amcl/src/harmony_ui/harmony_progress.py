# harmony_progress.py
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen
from PySide6.QtWidgets import QWidget
from harmony_theme import HarmonyTheme


class HarmonyProgressBar(QWidget):
    """鸿蒙风格进度条"""

    value_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 进度属性
        self._value = 0
        self._minimum = 0
        self._maximum = 100

        # 外观配置
        self._height = 8
        self._radius = 4

        # 颜色配置
        self._track_color = QColor(HarmonyTheme.BackgroundTertiary)
        self._progress_color = QColor(HarmonyTheme.PrimaryColor)
        self._buffer_color = QColor(HarmonyTheme.PrimaryColor).lighter(150)

        # 动画
        self._progress_animation = QPropertyAnimation(self, b"animated_value")
        self._progress_animation.setDuration(500)
        self._progress_animation.setEasingCurve(QEasingCurve.OutCubic)

        self._animated_value = 0

        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(self._height)
        self.setMinimumWidth(200)

    def animated_value(self):
        return getattr(self, '_animated_value', 0)

    def set_animated_value(self, value):
        self._animated_value = value
        self.update()
        
    animated_value = Property(float, animated_value, set_animated_value)

    def paintEvent(self, event):
        """绘制进度条"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制轨道
        self._draw_track(painter)

        # 绘制进度
        self._draw_progress(painter)

        # 绘制缓冲条（可选）
        # self._draw_buffer(painter)

    def _draw_track(self, painter: QPainter):
        """绘制轨道"""
        track_rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(self._track_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(track_rect, self._radius, self._radius)

    def _draw_progress(self, painter: QPainter):
        """绘制进度"""
        if self._animated_value > 0:
            progress_width = int(self.width() * self._animated_value / 100)
            progress_rect = QRect(0, 0, progress_width, self.height())

            painter.setBrush(QBrush(self._progress_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(progress_rect, self._radius, self._radius)

    def set_value(self, value: int):
        """设置进度值"""
        value = max(self._minimum, min(self._maximum, value))
        if self._value != value:
            self._value = value
            self._animate_progress()
            self.value_changed.emit(value)

    def _animate_progress(self):
        """动画进度"""
        self._progress_animation.setStartValue(self._animated_value)
        self._progress_animation.setEndValue(self._value)
        self._progress_animation.start()

    def set_range(self, minimum: int, maximum: int):
        """设置范围"""
        self._minimum = minimum
        self._maximum = maximum
        self.update()

    def get_value(self):
        """获取当前值"""
        return self._value

    def get_percentage(self):
        """获取百分比"""
        if self._maximum - self._minimum == 0:
            return 0
        return (self._value - self._minimum) * 100 / (self._maximum - self._minimum)


class HarmonyCircularProgress(QWidget):
    """鸿蒙风格环形进度条"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._value = 0
        self._minimum = 0
        self._maximum = 100
        self._line_width = 6
        self._progress_color = QColor(HarmonyTheme.PrimaryColor)
        self._track_color = QColor(HarmonyTheme.BackgroundTertiary)

        self.setFixedSize(120, 120)

    def paintEvent(self, event):
        """绘制环形进度条"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算几何
        rect = self.rect()
        size = min(rect.width(), rect.height())
        margin = self._line_width // 2

        # 绘制轨道
        painter.setPen(QPen(self._track_color, self._line_width, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(rect.center(), size // 2 - margin, size // 2 - margin)

        # 绘制进度
        if self._value > 0:
            angle = int(360 * self._value / (self._maximum - self._minimum))
            painter.setPen(QPen(self._progress_color, self._line_width, Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(margin, margin, size - 2 * margin, size - 2 * margin,
                            90 * 16, -angle * 16)

    def set_value(self, value: int):
        """设置进度值"""
        value = max(self._minimum, min(self._maximum, value))
        if self._value != value:
            self._value = value
            self.update()

    def set_line_width(self, width: int):
        """设置线宽"""
        self._line_width = width
        self.update()

    def set_colors(self, progress_color: QColor, track_color: QColor):
        """设置颜色"""
        self._progress_color = progress_color
        self._track_color = track_color
        self.update()