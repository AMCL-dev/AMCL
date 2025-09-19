# harmony_input.py
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QEnterEvent, QFocusEvent
from PySide6.QtWidgets import QLineEdit, QTextEdit, QGraphicsDropShadowEffect
from harmony_theme import HarmonyTheme


class HarmonyLineEdit(QLineEdit):
    """鸿蒙风格输入框"""

    focus_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 状态属性
        self._is_focused = False
        self._is_hovered = False

        # 颜色配置
        self._normal_border = QColor(HarmonyTheme.BorderMedium)
        self._hover_border = QColor(HarmonyTheme.PrimaryColor)
        self._focus_border = QColor(HarmonyTheme.PrimaryColor)
        self._error_border = QColor("#EF4444")

        self._setup_ui()
        self._setup_animations()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(48)
        self.setStyleSheet(self._get_style_sheet())

    def _setup_animations(self):
        """设置动画"""
        self._border_animation = QPropertyAnimation(self, b"styleSheet")
        self._border_animation.setDuration(200)
        self._border_animation.setEasingCurve(QEasingCurve.OutCubic)

    def _get_style_sheet(self):
        """获取样式表"""
        border_color = self._normal_border.name()

        if self._is_focused:
            border_color = self._focus_border.name()
        elif self._is_hovered:
            border_color = self._hover_border.name()

        return f"""
            QLineEdit {{
                background-color: {HarmonyTheme.BackgroundPrimary};
                color: {HarmonyTheme.TextPrimary};
                border: 2px solid {border_color};
                border-radius: {HarmonyTheme.BorderRadiusMedium}px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
            }}
            QLineEdit:focus {{
                border-color: {self._focus_border.name()};
                background-color: {HarmonyTheme.BackgroundPrimary};
            }}
            QLineEdit:disabled {{
                background-color: {HarmonyTheme.BackgroundTertiary};
                color: {HarmonyTheme.TextTertiary};
                border-color: {HarmonyTheme.BorderLight};
            }}
            QLineEdit::placeholder {{
                color: {HarmonyTheme.TextTertiary};
            }}
        """

    def enterEvent(self, event: QEnterEvent):
        """鼠标进入"""
        super().enterEvent(event)
        self._is_hovered = True
        self.setStyleSheet(self._get_style_sheet())

    def leaveEvent(self, event):
        """鼠标离开"""
        super().leaveEvent(event)
        self._is_hovered = False
        self.setStyleSheet(self._get_style_sheet())

    def focusInEvent(self, event: QFocusEvent):
        """获得焦点"""
        super().focusInEvent(event)
        self._is_focused = True
        self.setStyleSheet(self._get_style_sheet())
        self.focus_changed.emit(True)

    def focusOutEvent(self, event: QFocusEvent):
        """失去焦点"""
        super().focusOutEvent(event)
        self._is_focused = False
        self.setStyleSheet(self._get_style_sheet())
        self.focus_changed.emit(False)

    def set_error(self, is_error: bool):
        """设置错误状态"""
        if is_error:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {HarmonyTheme.BackgroundPrimary};
                    color: {HarmonyTheme.TextPrimary};
                    border: 2px solid {self._error_border.name()};
                    border-radius: {HarmonyTheme.BorderRadiusMedium}px;
                    padding: 12px 16px;
                    font-size: 14px;
                }}
            """)
        else:
            self.setStyleSheet(self._get_style_sheet())


class HarmonyTextEdit(QTextEdit):
    """鸿蒙风格文本域"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {HarmonyTheme.BackgroundPrimary};
                color: {HarmonyTheme.TextPrimary};
                border: 2px solid {HarmonyTheme.BorderMedium};
                border-radius: {HarmonyTheme.BorderRadiusMedium}px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
                selection-background-color: {HarmonyTheme.PrimaryColor};
                selection-color: #FFFFFF;
            }}
            QTextEdit:focus {{
                border-color: {HarmonyTheme.PrimaryColor};
            }}
            QTextEdit::placeholder {{
                color: {HarmonyTheme.TextTertiary};
            }}
        """)