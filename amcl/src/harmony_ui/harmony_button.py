# harmony_button.py
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QEnterEvent, QMouseEvent
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from harmony_theme import HarmonyTheme
from harmony_widget_base import HarmonyWidgetBase


class HarmonyPushButton(QPushButton):
    """鸿蒙风格按钮"""

    clicked = Signal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # 状态属性
        self._is_hovered = False
        self._is_pressed = False
        self._is_disabled = False

        # 颜色状态
        self._normal_color = QColor(HarmonyTheme.PrimaryColor)
        self._hover_color = QColor(HarmonyTheme.PrimaryHover)
        self._pressed_color = QColor(HarmonyTheme.PrimaryPressed)
        self._disabled_color = QColor("#E5E7EB")
        self._text_color = QColor("#FFFFFF")

        # 动画
        self._bg_animation = QPropertyAnimation(self, b"current_color")
        self._bg_animation.setDuration(200)
        self._bg_animation.setEasingCurve(QEasingCurve.OutCubic)

        self._setup_ui()
        self._setup_shadow()

    def _setup_ui(self):
        """设置UI"""
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(48)
        self.setStyleSheet(self._get_style_sheet())

    def _setup_shadow(self):
        """设置阴影"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def _get_style_sheet(self):
        """获取样式表"""
        return f"""
            QPushButton {{
                background-color: {self._normal_color.name()};
                color: {self._text_color.name()};
                border: none;
                border-radius: {HarmonyTheme.BorderRadiusMedium}px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
            }}
            QPushButton:pressed {{
                background-color: {self._pressed_color.name()};
                padding-top: 13px;
                padding-bottom: 11px;
            }}
            QPushButton:disabled {{
                background-color: {self._disabled_color.name()};
                color: #9CA3AF;
            }}
        """

    def enterEvent(self, event: QEnterEvent):
        """鼠标进入"""
        super().enterEvent(event)
        self._is_hovered = True
        self._update_style()

    def leaveEvent(self, event):
        """鼠标离开"""
        super().leaveEvent(event)
        self._is_hovered = False
        self._is_pressed = False
        self._update_style()

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._is_pressed = True
            self._update_style()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放"""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self._is_pressed = False
            self._update_style()
            if self.rect().contains(event.pos()):
                self.clicked.emit()

    def _update_style(self):
        """更新样式"""
        self.setStyleSheet(self._get_style_sheet())

    def set_button_type(self, button_type: str):
        """设置按钮类型"""
        if button_type == "primary":
            self._normal_color = QColor(HarmonyTheme.PrimaryColor)
            self._hover_color = QColor(HarmonyTheme.PrimaryHover)
            self._pressed_color = QColor(HarmonyTheme.PrimaryPressed)
            self._text_color = QColor("#FFFFFF")
        elif button_type == "secondary":
            self._normal_color = QColor("#F3F4F6")
            self._hover_color = QColor("#E5E7EB")
            self._pressed_color = QColor("#D1D5DB")
            self._text_color = QColor(HarmonyTheme.TextPrimary)
        elif button_type == "text":
            self._normal_color = QColor("transparent")
            self._hover_color = QColor("#F3F4F6")
            self._pressed_color = QColor("#E5E7EB")
            self._text_color = QColor(HarmonyTheme.PrimaryColor)

        self._update_style()


class HarmonyIconButton(HarmonyPushButton):
    """鸿蒙风格图标按钮"""

    def __init__(self, icon_text="", parent=None):
        super().__init__(icon_text, parent)
        self.setFixedSize(48, 48)
        self.setStyleSheet(self._get_icon_style())

    def _get_icon_style(self):
        """获取图标按钮样式"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {HarmonyTheme.TextSecondary};
                border: none;
                border-radius: {HarmonyTheme.BorderRadiusMedium}px;
                font-size: 20px;
                font-family: "Segoe Fluent Icons", "Segoe MDL2 Assets";
            }}
            QPushButton:hover {{
                background-color: {HarmonyTheme.BackgroundTertiary};
                color: {HarmonyTheme.TextPrimary};
            }}
            QPushButton:pressed {{
                background-color: {HarmonyTheme.BackgroundSecondary};
                color: {HarmonyTheme.PrimaryColor};
            }}
        """