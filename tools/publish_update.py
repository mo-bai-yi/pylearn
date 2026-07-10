"""Pylearn 一键发布更新脚本

将新版内容打包推送到 gh-pages 分支，作为 Pylearn 客户端的更新源。

用法：
    # 1. 先修改 content/、templates/、static/ 里的文件，然后：
    python tools/publish.py

    # 2. 脚本会：
    #    - 自动读取当前 version.json
    #    - 构建更新包到临时目录
    #    - 推送到 GitHub Pages 分支
    #    - 用户打开 Pylearn → 设置 → 检查更新 → 下载

    # 强制更新版本号（不改 version.json 也能发布）：
    python tools/publish.py --bump minor    # 1.0.0 → 1.1.0
    python tools/publish.py --bump major    # 1.0.0 → 2.0.0
    python tools/publish.py --bump patch    # 1.0.0 → 1.0.1
    python tools/publish.py --set 2.0.0     # 直接设成指定版本
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
VERSION_FILE = HERE / 'version.json'

# 需要发布的目录
PUBLISH_DIRS = ['content', 'templates', 'static']
# 额外需要发布的根目录文件
PUBLISH_FILES = ['version.json']


def bump_version(current: str, part: str) -> str:
    """版本号递增"""
    parts = [int(x) for x in current.split('.')]
    if part == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif part == 'minor':
        parts[1] += 1
        parts[2] = 0
    elif part == 'patch':
        parts[2] += 1
    else:
        raise ValueError(f'未知版本段: {part}')
    return '.'.join(str(p) for p in parts)


def build_update_package(target_dir: Path, new_version: str | None, changelog: str):
    """构建更新包到 target_dir"""
    # 读取当前版本信息
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        version_info = json.load(f)

    old_version = version_info['version']
    version = new_version or old_version

    if new_version:
        version_info['version'] = version
        version_info['updated'] = '2026-07-10'  # 实际使用时可改为当前日期

    if changelog:
        version_info['changelog'] = changelog
    elif 'changelog' not in version_info:
        version_info['changelog'] = f'🔄 更新至 v{version}'

    # 收集文件列表
    file_list = []

    # 复制每个目录
    for dirname in PUBLISH_DIRS:
        src = HERE / dirname
        dst = target_dir / dirname
        if src.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for f in dst.rglob('*'):
                if f.is_file():
                    rel = str(f.relative_to(target_dir))
                    file_list.append(rel)

    # 复制根目录文件
    for fname in PUBLISH_FILES:
        src = HERE / fname
        if src.exists():
            shutil.copy2(src, target_dir / fname)

    # 更新 version.json（写入最新文件列表）
    version_info['files'] = file_list
    version_info['has_exe'] = False

    with open(target_dir / 'version.json', 'w', encoding='utf-8') as f:
        json.dump(version_info, f, ensure_ascii=False, indent=2)

    return version_info, file_list


def publish_to_gh_pages(target_dir: Path, version_info: dict):
    """将更新包推送到 gh-pages 分支"""
    import subprocess

    old_cwd = os.getcwd()
    os.chdir(HERE)

    # 支持 GITHUB_TOKEN 环境变量认证
    token = os.environ.get('GITHUB_TOKEN')
    push_url = None
    if token:
        # 获取当前 remote 地址，嵌入 token
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True, check=True)
        base_url = result.stdout.strip()
        if base_url.startswith('https://'):
            push_url = base_url.replace('https://', f'https://oauth2:{token}@')

    try:
        # 检查 git 状态
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print('⚠️  工作区有未提交的修改，先提交再发布：')
            print(result.stdout)
            return False

        # 切换到 gh-pages 分支（或创建）
        result = subprocess.run(['git', 'rev-parse', '--verify', 'gh-pages'], capture_output=True, text=True)
        if result.returncode == 0:
            # gh-pages 已存在，切换过去
            subprocess.run(['git', 'checkout', 'gh-pages'], check=True)
        else:
            # 创建 gh-pages 分支（孤儿分支）
            subprocess.run(['git', 'checkout', '--orphan', 'gh-pages'], check=True)
            # 清理工作区
            subprocess.run(['git', 'rm', '-rf', '.'], capture_output=True)

        # 清空工作区（保留 .git）
        for item in Path('.').iterdir():
            if item.name != '.git' and item.name != target_dir.name:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink()

        # 复制更新包到工作区根目录
        for item in target_dir.iterdir():
            dst = HERE / item.name
            if item.is_dir():
                shutil.copytree(item, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst)

        # 提交并推送
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', f'发布 v{version_info["version"]}'], check=True)
        push_cmd = ['git', 'push', 'origin', 'gh-pages', '--force']
        if push_url:
            push_cmd = ['git', 'push', push_url, 'gh-pages', '--force']
        subprocess.run(push_cmd, check=True)

        print(f'✅ 已推送到 gh-pages 分支')
        return True

    except subprocess.CalledProcessError as e:
        print(f'❌ Git 操作失败: {e}')
        return False
    finally:
        os.chdir(old_cwd)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pylearn 一键发布更新')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'],
                        help='自动递增版本号')
    parser.add_argument('--set', help='直接指定版本号')
    parser.add_argument('--changelog', '-m', help='更新日志')
    args = parser.parse_args()

    # 确定新版本号
    new_version = None
    if args.bump:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            current = json.load(f)['version']
        new_version = bump_version(current, args.bump)
    elif args.set:
        new_version = args.set

    # 构建更新包到临时目录
    tmpdir = Path(tempfile.mkdtemp(prefix='pylearn-publish-'))
    try:
        version_info, file_list = build_update_package(tmpdir, new_version, args.changelog)

        print(f'📦 更新包构建完成')
        print(f'   版本: {version_info["version"]}')
        print(f'   文件数: {len(file_list)}')
        print(f'   更新日志: {version_info.get("changelog", "无")}')
        print()

        # 推送到 gh-pages
        print('🚀 正在推送到 GitHub Pages...')
        success = publish_to_gh_pages(tmpdir, version_info)

        if success:
            update_url = 'https://mo-bai-yi.github.io/pylearn/'
            print()
            print(f'🔗 更新源地址: {update_url}')
            print(f'📄 版本文件:   {update_url}version.json')
            print()
            print('用户打开 Pylearn → 设置 → 点"检查更新"即可获取')
        else:
            sys.exit(1)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == '__main__':
    main()
