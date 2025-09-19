# harmony_theme.py
from PySide6.QtCore import QObject, Property, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QColor, QPalette


class HarmonyTheme(QObject):
    """鸿蒙主题配色系统"""

    # 主色调
    PrimaryColor = "#007DFF"  # 华为蓝
    PrimaryHover = "#0059B3"
    PrimaryPressed = "#004A99"

    # 背景色
    BackgroundPrimary = "#FFFFFF"
    BackgroundSecondary = "#F5F7FA"
    BackgroundTertiary = "#F0F2F5"

    # 文字颜色
    TextPrimary = "#121212"
    TextSecondary = "#595959"
    TextTertiary = "#8C8C8C"

    # 边框颜色
    BorderLight = "#E6E8EB"
    BorderMedium = "#D1D5DB"
    BorderDark = "#9CA3AF"

    # 圆角半径
    BorderRadiusSmall = 8
    BorderRadiusMedium = 12
    BorderRadiusLarge = 16

    # 阴影
    ShadowColor = QColor(0, 0, 0, 25)
    ShadowBlurRadius = 12
    ShadowOffset = (0, 4)

    @staticmethod
    def get_button_style(normal_color, hover_color, pressed_color,
                         text_color="#FFFFFF", radius=12):
        """获取按钮样式表"""
        return f"""
            QPushButton {{
                background-color: {normal_color};
                color: {text_color};
                border: none;
                border-radius: {radius}px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #E5E7EB;
                color: #9CA3AF;
            }}
        """