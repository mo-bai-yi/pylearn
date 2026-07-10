"""首页路由"""

from flask import Blueprint, render_template
from app.utils.content_loader import get_lessons
from app.db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    lessons = get_lessons()
    # 统计完成进度
    try:
        db = get_db()
        completed = db.execute(
            'SELECT COUNT(*) as c FROM lesson_progress WHERE completed = 1'
        ).fetchone()['c']
    except Exception:
        completed = 0

    return render_template('index.html',
                           title='Pylearn',
                           lessons=lessons,
                           completed=completed,
                           total=len(lessons))
