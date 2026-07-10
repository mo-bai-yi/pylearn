"""安全代码执行器——在子进程中运行用户代码"""

import sys
import subprocess
import tempfile
import os
import ast

# 黑名单：禁止导入的模块
BLOCKED_IMPORTS = {
    'os', 'subprocess', 'shutil', 'sys',
    'importlib', 'ctypes', 'socket', 'requests',
    'http', 'urllib', 'pathlib', 'glob',
    'multiprocessing', 'threading', 'signal',
    'pickle', 'shelve', 'dbm',
    'webbrowser', 'antigravity',
    'tkinter', 'PyQt5', 'PySide',
}

# 临时工作目录
TEMP_DIR = tempfile.mkdtemp(prefix='pylearn_')


def _check_dangerous_code(source: str):
    """静态检查是否有危险代码"""
    # 检查黑名单 import
    for mod in BLOCKED_IMPORTS:
        if f'import {mod}' in source or f'from {mod}' in source:
            return f'🚫 模块 "{mod}" 已禁用（安全限制）'

    # 检查危险内置函数
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ('eval', 'exec', 'compile', '__import__', 'open'):
                        return f'🚫 函数 "{node.func.id}()" 已禁用（安全限制）'
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in ('system', 'popen', 'run', 'check_output'):
                        return f'🚫 危险调用已禁用'
    except SyntaxError:
        pass  # 让 Python 自己报语法错误

    return None


def run_code(source: str, timeout: int = 5):
    """执行用户代码

    Args:
        source: Python 源代码字符串
        timeout: 超时秒数（默认 5s）

    Returns:
        dict: {stdout, stderr, returncode, error}
    """
    # 安全检查
    danger = _check_dangerous_code(source)
    if danger:
        return {
            'stdout': '',
            'stderr': danger,
            'returncode': -1,
            'error': danger,
        }

    # 捕获 print 输出并运行
    try:
        result = subprocess.run(
            [sys.executable, '-c', source],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=TEMP_DIR,
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'error': None,
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': '',
            'returncode': -1,
            'error': f'⏱️ 代码执行超过 {timeout} 秒，已自动终止',
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
            'error': f'❌ 执行出错：{str(e)}',
        }
