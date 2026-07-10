"""内容加载器——读取教程和关卡定义"""

import os
import glob
from app.path_utils import get_content_dir


def _lessons_dir():
    return get_content_dir('lessons')


def get_lessons():
    """获取所有教程列表，按文件名排序"""
    files = sorted(glob.glob(os.path.join(_lessons_dir(), '*.md')))
    lessons = []
    for f in files:
        name = os.path.basename(f).replace('.md', '')
        with open(f, 'r', encoding='utf-8') as fh:
            first_line = fh.readline().strip()
        if first_line.startswith('# '):
            title = first_line[2:].strip()
        else:
            title = name
        lessons.append({
            'id': name,
            'title': title,
            'file': f,
        })
    return lessons


def get_lesson(lesson_id: str):
    """获取单篇教程内容"""
    filepath = os.path.join(_lessons_dir(), f'{lesson_id}.md')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.strip().split('\n')
    title = lines[0].lstrip('#').strip() if lines else lesson_id
    return {
        'id': lesson_id,
        'title': title,
        'content': content,
    }
