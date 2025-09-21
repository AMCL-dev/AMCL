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

import sys
from pathlib import Path


def r(relative_path):
    # the packaged environment
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable)
    # the development environment
    else:
        base_path = Path(__file__).resolve().parent.parent.parent.parent

    return str(base_path / relative_path)