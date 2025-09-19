#!/usr/bin/env python3
import subprocess
import sys


def install_dependencies():
    """安装构建依赖"""
    dependencies = [
        "nuitka",
        "ordered-set",
        "setuptools"
    ]

    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
    install_dependencies()