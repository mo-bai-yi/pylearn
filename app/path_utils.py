"""路径工具——支持源码模式和 PyInstaller 打包模式"""

import sys
import os


def get_app_root():
    """获取应用根目录

    - 源码模式：项目根目录（pylearn/）
    - 打包模式：exe 所在目录
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包模式
        return os.path.dirname(sys.executable)
    else:
        # 开发模式：app/../.. 即项目根目录
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_content_dir(subdir=''):
    """获取内容目录（lessons/ 或 challenges/ 的父级）"""
    base = os.path.join(get_app_root(), 'content')
    if subdir:
        return os.path.join(base, subdir)
    return base
