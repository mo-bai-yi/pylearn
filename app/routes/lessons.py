"""教程模块路由"""

from flask import Blueprint, render_template, abort
from app.utils.content_loader import get_lessons, get_lesson

bp = Blueprint('lessons', __name__)


@bp.route('/')
def lesson_list():
    lessons = get_lessons()
    return render_template('lessons/list.html',
                           title='教程目录',
                           lessons=lessons)


@bp.route('/<lesson_id>')
def lesson_view(lesson_id):
    lesson = get_lesson(lesson_id)
    if not lesson:
        abort(404)
    lessons = get_lessons()
    # 找前后章节
    ids = [l['id'] for l in lessons]
    idx = ids.index(lesson_id)
    prev_lesson = lessons[idx - 1] if idx > 0 else None
    next_lesson = lessons[idx + 1] if idx < len(lessons) - 1 else None

    return render_template('lessons/view.html',
                           title=lesson['title'],
                           lesson=lesson,
                           prev=prev_lesson,
                           next=next_lesson)
