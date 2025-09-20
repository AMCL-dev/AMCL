import sys
from pathlib import Path


def r(relative_path):
    # the packaged environment
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent.parent
    # the development environment
    else:
        base_path = Path(__file__).resolve().parent.parent.parent.parent

    return str(base_path / relative_path)