# harmony_card.py
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QEnterEvent
from PySide6.QtWidgets import QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from harmony_ui.harmony_theme import HarmonyTheme
from harmony_ui.harmony_widget_base import HarmonyWidgetBase


class HarmonyCard(HarmonyWidgetBase):
    """鸿蒙风格卡片组件"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 卡片属性
        self._elevation = 1
        self._hover_elevation = 3
        self._is_hovered = False

        # 颜色配置
        self._background_color = QColor(HarmonyTheme.BackgroundPrimary)
        self._border_color = QColor(HarmonyTheme.BorderLight)

        self._setup_ui()
        self._setup_animations()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(200)
        self.setMinimumWidth(300)

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        # 设置样式
        self.setStyleSheet(f"""
            HarmonyCard {{
                background-color: {HarmonyTheme.BackgroundPrimary};
                border: 1px solid {HarmonyTheme.BorderLight};
                border-radius: {HarmonyTheme.BorderRadiusLarge}px;
            }}
        """)

    def _setup_animations(self):
        """设置动画"""
        self._shadow_animation = QPropertyAnimation(self.graphicsEffect(), b"blurRadius")
        self._shadow_animation.setDuration(200)
        self._shadow_animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event: QEnterEvent):
        """鼠标进入"""
        super().enterEvent(event)
        self._is_hovered = True
        self._animate_shadow(self._hover_elevation)

    def leaveEvent(self, event):
        """鼠标离开"""
        super().leaveEvent(event)
        self._is_hovered = False
        self._animate_shadow(self._elevation)

    def _animate_shadow(self, elevation: int):
        """动画阴影"""
        if self.graphicsEffect():
            start_blur = self.graphicsEffect().blurRadius()
            end_blur = elevation * 4

            self._shadow_animation.setStartValue(start_blur)
            self._shadow_animation.setEndValue(end_blur)
            self._shadow_animation.start()

    def set_elevation(self, elevation: int):
        """设置阴影深度"""
        self._elevation = elevation
        if not self._is_hovered:
            self._animate_shadow(elevation)

    def add_widget(self, widget):
        """添加子组件"""
        self.main_layout.addWidget(widget)