"""本地热更新测试服务器

启动一个 HTTP 服务模拟远程更新源。
把想要"推送更新"的文件放在 update_dist/ 目录下。

用法：
    python tools/update_server.py              # 启动（默认 8000 端口）
    python tools/update_server.py --port 9000  # 指定端口

测试步骤：
    1. 启动此服务：python tools/update_server.py
    2. 设置环境变量：export PYLEARN_UPDATE_URL=http://127.0.0.1:8000
    3. 重启 Pylearn
    4. 访问 /settings 点击"检查更新"

模拟推送更新：
    修改 update_dist/version.json 中的版本号，
    或在 update_dist/content/lessons/ 下修改教程内容，
    然后重启此服务，Pylearn 里点"检查更新"就能看到新版本。
"""

import os
import json
import shutil
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# 更新源根目录
HERE = Path(__file__).resolve().parent.parent
UPDATE_DIST = HERE / 'update_dist'


def prepare_test_data():
    """准备测试用的更新数据"""
    if UPDATE_DIST.exists():
        shutil.rmtree(UPDATE_DIST)

    # 从当前项目复制一份作为"旧版本"
    shutil.copytree(HERE / 'content', UPDATE_DIST / 'content')
    shutil.copytree(HERE / 'templates', UPDATE_DIST / 'templates')
    shutil.copytree(HERE / 'static', UPDATE_DIST / 'static')

    # 创建版本文件
    version = {
        "version": "1.1.0",
        "name": "Pylearn",
        "changelog": "🆕 新增字典/元组/文件/异常章节\n🐛 修复Turtle画板无线条bug\n💄 界面放大10%\n📦 支持热更新",
        "has_exe": False,
        "files": []
    }

    # 列出所有文件
    for dirname in ['content', 'templates', 'static']:
        target = UPDATE_DIST / dirname
        if target.exists():
            for f in target.rglob('*'):
                if f.is_file() and '__pycache__' not in f.parts:
                    version['files'].append(str(f.relative_to(UPDATE_DIST)))

    with open(UPDATE_DIST / 'version.json', 'w', encoding='utf-8') as f:
        json.dump(version, f, ensure_ascii=False, indent=2)

    print(f"📦 更新源已准备: {UPDATE_DIST}")
    print(f"   版本: {version['version']}")
    print(f"   文件数: {len(version['files'])}")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UPDATE_DIST), **kwargs)

    def log_message(self, format, *args):
        print(f"  [{self.log_date_time_string()}] {args[0]} {args[1]} {args[2]}")


def main():
    port = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8000

    # 准备测试数据
    if not UPDATE_DIST.exists():
        prepare_test_data()
    else:
        # 更新文件列表（因为本地文件可能变了）
        version_file = UPDATE_DIST / 'version.json'
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                version = json.load(f)
            files = []
            for dirname in ['content', 'templates', 'static']:
                target = UPDATE_DIST / dirname
                if target.exists():
                    for f in target.rglob('*'):
                        if f.is_file() and '__pycache__' not in f.parts:
                            files.append(str(f.relative_to(UPDATE_DIST)))
            version['files'] = files
            with open(version_file, 'w', encoding='utf-8') as f:
                json.dump(version, f, ensure_ascii=False, indent=2)

    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"\n🚀 更新测试服务已启动: http://127.0.0.1:{port}")
    print(f"   版本文件: http://127.0.0.1:{port}/version.json")
    print(f"\n   设置环境变量后重启 Pylearn：")
    print(f"   export PYLEARN_UPDATE_URL=http://127.0.0.1:{port}")
    print(f"\n   按 Ctrl+C 停止\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()


if __name__ == '__main__':
    main()
