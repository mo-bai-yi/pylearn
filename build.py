"""Pylearn 构建脚本——打包为可更新的桌面 exe

用法：
    python build.py              # 打包
    python build.py --browser    # 打包为浏览器模式（不加 --windowed）
    python build.py --clean      # 清理

打包后生成 dist/pylearn/ 目录，结构：
    pylearn.exe          ← 主程序（替换此文件即可更新代码）
    _internal/           ← Python 运行时
    content/             ← 教程/闯关（可独立更新）
    templates/           ← 页面模板（可独立更新）
    static/              ← CSS/JS（可独立更新）
    version.json         ← 版本信息

在 Windows 上运行此脚本才能生成真正的 .exe。
"""

import os
import sys
import shutil
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')
SPEC_FILE = os.path.join(PROJECT_DIR, 'pylearn.spec')
UPDATEABLE_DIRS = ['content', 'templates', 'static']


def clean():
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  删除: {d}")
    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"  删除: {SPEC_FILE}")
    print("✅ 清理完成")


def build():
    print("🚀 打包 Pylearn...\n")
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)

    is_windows = os.name == 'nt'

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onedir',
        '--name', 'pylearn',
        '--distpath', DIST_DIR,
        '--workpath', BUILD_DIR,
        '--add-data', f'version.json{os.pathsep}.',
        '--hidden-import', 'yaml',
        '--hidden-import', 'flask',
        '--hidden-import', 'webview',
        '--collect-all', 'flask',
        'run.py',
    ]

    # 桌面模式：Windows 下隐藏黑窗口，Linux/mac 不需要
    if is_windows and '--browser' not in sys.argv:
        cmd.append('--windowed')
        print("  模式: 桌面窗口")
    else:
        print("  模式: 浏览器（--windowed 未启用）")

    result = subprocess.run(cmd, cwd=PROJECT_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ 打包失败:")
        print(result.stderr[-1500:])
        sys.exit(1)

    dist_app = os.path.join(DIST_DIR, 'pylearn')

    # 复制可更新目录到 exe 旁边
    print("\n📂 复制可更新资源...")
    for dirname in UPDATEABLE_DIRS:
        src = os.path.join(PROJECT_DIR, dirname)
        dst = os.path.join(dist_app, dirname)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__'))
            size = sum(os.path.getsize(os.path.join(dp, f))
                      for dp, dn, fn in os.walk(dst) for f in fn)
            print(f"   {dirname}/  {size//1024}KB")

    # 版本文件
    shutil.copy2(os.path.join(PROJECT_DIR, 'version.json'), dist_app)

    exe_path = os.path.join(dist_app, 'pylearn.exe' if is_windows else 'pylearn')
    total = sum(os.path.getsize(os.path.join(dp, f))
               for dp, dn, fn in os.walk(dist_app) for f in fn)

    print(f"\n✅ 打包完成！")
    print(f"   位置: {dist_app}")
    print(f"   大小: {total // 1024 // 1024} MB")
    print(f"   启动: {exe_path}")
    print(f"\n📦 分发：将 dist/pylearn/ 整个文件夹压缩发给用户")
    print(f"🔄 更新：替换 pylearn.exe（代码）或 content/（教程）")


if __name__ == '__main__':
    if '--clean' in sys.argv:
        clean()
    else:
        build()
