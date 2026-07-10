"""安全代码执行器——在子进程中运行用户代码"""

import sys
import subprocess
import tempfile
import os
import ast

# 获取合适的 Python 解释器路径
def _get_python_exe():
    """获取可用的 Python 解释器（兼容 PyInstaller 打包的 exe）"""
    # 如果是打包后的 exe，sys.executable 是 pylearn.exe 本身
    if getattr(sys, 'frozen', False):
        # 1. 优先找打包目录里的 _internal/python.exe
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            bundled = os.path.join(meipass, 'python.exe')
            if os.path.exists(bundled):
                return bundled

        # 2. 找系统 PATH 里的 python
        for name in ['python.exe', 'python3.exe', 'python']:
            found = subprocess.run(['where', name] if os.name == 'nt' else ['which', name],
                                  capture_output=True, text=True, timeout=3)
            if found.returncode == 0:
                exe_path = found.stdout.strip().split('\n')[0]
                # 避免找到自己（同一个 exe）
                if os.path.normpath(exe_path) != os.path.normpath(sys.executable):
                    return exe_path

        # 3. 最后尝试 python in-process（功能受限但能用）
        return None
    else:
        # 正常 Python 环境
        return sys.executable


# 缓存 Python 解释器路径
_PYTHON_EXE = _get_python_exe()

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


def _run_in_process(source: str, timeout: int = 5):
    """在进程内执行代码（找不到外部 Python 时的回退方案）"""
    import io
    import contextlib
    import threading

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    result = {'stdout': '', 'stderr': '', 'returncode': 0, 'error': None}

    def _exec():
        try:
            # 受限的 globals，不暴露危险模块
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'range': range,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'type': type,
                    'True': True,
                    'False': False,
                    'None': None,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'round': round,
                    'sorted': sorted,
                    'reversed': reversed,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    'any': any,
                    'all': all,
                    'isinstance': isinstance,
                    'hasattr': hasattr,
                    'getattr': getattr,
                    'setattr': setattr,
                    'input': input,
                    'iter': iter,
                    'next': next,
                    'repr': repr,
                    'ord': ord,
                    'chr': chr,
                    'hex': hex,
                    'oct': oct,
                    'bin': bin,
                },
                # 允许 math/random/json
                'math': __import__('math'),
                'random': __import__('random'),
                'json': __import__('json'),
                'datetime': __import__('datetime'),
                'string': __import__('string'),
                'collections': __import__('collections'),
                'itertools': __import__('itertools'),
                'functools': __import__('functools'),
                're': __import__('re'),
                'decimal': __import__('decimal'),
                'fractions': __import__('fractions'),
                'statistics': __import__('statistics'),
                'turtle': __import__('turtle'),
            }
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(source, safe_globals)
        except Exception as e:
            stderr_buf.write(f'{type(e).__name__}: {e}')

    thread = threading.Thread(target=_exec, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return {'stdout': '', 'stderr': '', 'returncode': -1,
                'error': f'⏱️ 代码执行超过 {timeout} 秒，已自动终止'}

    result['stdout'] = stdout_buf.getvalue()
    result['stderr'] = stderr_buf.getvalue()
    return result


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
        if _PYTHON_EXE:
            result = subprocess.run(
                [_PYTHON_EXE, '-c', source],
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
        else:
            # 找不到外部 Python，在进程内执行（有限沙箱）
            return _run_in_process(source, timeout)
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
