"""设置/更新页面路由"""

from flask import Blueprint, render_template

bp = Blueprint('update', __name__)


@bp.route('/settings')
def settings():
    return render_template('settings.html', title='设置与更新')
