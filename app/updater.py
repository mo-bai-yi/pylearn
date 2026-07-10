"""热更新模块——检查更新、下载更新、应用更新

更新源可以是：
- HTTP 服务器（GitHub Pages / 任意静态服务器）
- 本地文件（开发测试用）

远程更新目录结构：
    version.json          ← 必须：版本信息 + 文件清单
    pylearn_new.exe       ← 可选：新 exe（改名后替换）
    content/...           ← 可选：更新的内容
    templates/...         ← 可选：更新的模板
    static/...            ← 可选：更新的静态资源
"""

import os
import json
import hashlib
import threading
from urllib.request import urlopen, Request
from urllib.error import URLError
from app.path_utils import get_app_root

# 更新源地址（GitHub Pages）
UPDATE_URL = 'https://mo-bai-yi.github.io/pylearn/'

UPDATE_INTERVAL = 3600  # 两次检查最短间隔（秒）

# 缓存
_last_check = 0
_last_result = None


def _file_hash(filepath):
    """计算文件 SHA256"""
    if not os.path.exists(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def _read_json(url_or_path):
    """读取 JSON（支持 URL 和本地路径）"""
    if url_or_path.startswith(('http://', 'https://')):
        req = Request(url_or_path, headers={'User-Agent': 'Pylearn-Updater/1.0'})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    else:
        with open(url_or_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def get_local_version():
    """读取本地版本信息"""
    path = os.path.join(get_app_root(), 'version.json')
    if not os.path.exists(path):
        return {'version': '0.0.0', 'name': 'Pylearn'}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_update(force=False):
    """检查远程是否有新版本

    Returns:
        dict: {
            'has_update': bool,
            'local_version': str,
            'remote_version': str,
            'changelog': str,
            'updatable': ['content', 'templates', 'static'],  # 可热更新的部分
            'has_new_exe': bool,  # 是否有新 exe
            'error': str | None,
        }
    """
    global _last_check, _last_result

    import time
    now = time.time()
    if not force and _last_result and (now - _last_check) < UPDATE_INTERVAL:
        return _last_result

    try:
        remote_ver_url = UPDATE_URL.rstrip('/') + '/version.json'
        remote = _read_json(remote_ver_url)
        local = get_local_version()

        rv = remote.get('version', '0.0.0')
        lv = local.get('version', '0.0.0')

        # 版本比较（简单字符串比较，建议用 semver 规范）
        has_update = rv != lv

        result = {
            'has_update': has_update,
            'local_version': lv,
            'remote_version': rv,
            'changelog': remote.get('changelog', ''),
            'has_new_exe': remote.get('has_exe', False),
            'error': None,
        }

        _last_check = now
        _last_result = result
        return result

    except URLError as e:
        return {'has_update': False, 'error': f'网络错误: {e.reason}'}
    except json.JSONDecodeError:
        return {'has_update': False, 'error': '远程版本文件格式错误'}
    except Exception as e:
        return {'has_update': False, 'error': str(e)}


def _download_file(relative_path, dest_dir):
    """从更新源下载单个文件"""
    url = UPDATE_URL.rstrip('/') + '/' + relative_path.replace('\\', '/')
    dest_path = os.path.join(dest_dir, relative_path)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    req = Request(url, headers={'User-Agent': 'Pylearn-Updater/1.0'})
    with urlopen(req, timeout=30) as resp:
        data = resp.read()

    # 先下载到 .tmp 再改名，防止中途中断导致文件损坏
    tmp_path = dest_path + '.tmp'
    with open(tmp_path, 'wb') as f:
        f.write(data)
    os.replace(tmp_path, dest_path)

    return dest_path


def apply_update(parts=None):
    """下载并应用更新

    Args:
        parts: ['content', 'templates', 'static'] 要更新的部分，None=全部

    Returns:
        dict: {'success': bool, 'updated': [文件名], 'error': str}
    """
    if parts is None:
        parts = ['content', 'templates', 'static']

    root = get_app_root()
    updated = []

    try:
        remote_ver_url = UPDATE_URL.rstrip('/') + '/version.json'
        remote = _read_json(remote_ver_url)
        file_list = remote.get('files', [])

        for rel_path in file_list:
            # 判断这个文件属于哪个部分
            matched = False
            for part in parts:
                if rel_path.startswith(part + '/'):
                    matched = True
                    break
            if not matched:
                continue

            _download_file(rel_path, root)
            updated.append(rel_path)

        return {'success': True, 'updated': updated, 'error': None}

    except Exception as e:
        return {'success': False, 'updated': updated, 'error': str(e)}


def download_new_exe():
    """下载新版本 exe（不立即替换，放在同目录下待重启时替换）

    Returns:
        dict: {'success': bool, 'path': str, 'error': str}
    """
    try:
        root = get_app_root()
        # 下载新 exe 到同目录，命名为 .new
        exe_name = 'pylearn.exe' if os.name == 'nt' else 'pylearn'
        new_exe_name = exe_name + '.new'

        dest = os.path.join(root, new_exe_name)
        url = UPDATE_URL.rstrip('/') + '/' + exe_name

        req = Request(url, headers={'User-Agent': 'Pylearn-Updater/1.0'})
        with urlopen(req, timeout=120) as resp:
            data = resp.read()

        tmp = dest + '.tmp'
        with open(tmp, 'wb') as f:
            f.write(data)
        os.replace(tmp, dest)

        # 创建重启脚本（Windows）
        if os.name == 'nt':
            bat_path = os.path.join(root, '_restart.bat')
            with open(bat_path, 'w') as f:
                f.write(f'''@echo off
timeout /t 2 /nobreak >nul
del "{os.path.join(root, exe_name)}"
move "{dest}" "{os.path.join(root, exe_name)}"
start "" "{os.path.join(root, exe_name)}"
del "%~f0"
''')

        return {'success': True, 'path': dest, 'error': None}

    except Exception as e:
        return {'success': False, 'path': '', 'error': str(e)}
