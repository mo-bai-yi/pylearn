"""代码演示台路由"""

from flask import Blueprint, render_template

bp = Blueprint('playground', __name__)


@bp.route('/playground')
def playground():
    return render_template('playground.html', title='代码演示台')
