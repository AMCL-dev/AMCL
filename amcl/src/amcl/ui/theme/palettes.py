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

from PySide6.QtGui import QColor

class BluePalette:
    name = "lightBlue"
    window      = QColor("#F0F4F8")
    surface     = QColor("#FFFFFF")
    primary     = QColor("#1E88E5")
    primaryText = QColor("#FFFFFF")
    text        = QColor("#212121")
    subText     = QColor("#757575")
    icon        = QColor("#212121")
    iconHover   = QColor("#1E88E5")

class DarkBluePalette:
    name = "darkBlue"
    window      = QColor("#121212")
    surface     = QColor("#1E1E1E")
    primary     = QColor("#90CAF9")
    primaryText = QColor("#000000")
    text        = QColor("#FFFFFF")
    subText     = QColor("#BDBDBD")
    icon        = QColor("#FFFFFF")
    iconHover   = QColor("#90CAF9")