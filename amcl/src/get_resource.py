import sys
from pathlib import Path


def get_resource_path(relative_path):
    # 在打包后的环境中，资源位于可执行文件所在目录
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    # 在开发环境中，资源位于项目根目录
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path