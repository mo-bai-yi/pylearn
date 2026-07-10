"""Turtle 可视化路由"""

from flask import Blueprint, render_template, request, jsonify
from app.utils.turtle_viz import parse_turtle_code, EXAMPLE_TURTLE_CODES

bp = Blueprint('turtle', __name__)


@bp.route('/turtle')
def turtle_page():
    return render_template('turtle.html',
                           title='Turtle 画板',
                           examples=EXAMPLE_TURTLE_CODES)


@bp.route('/turtle/parse', methods=['POST'])
def turtle_parse():
    """解析 turtle 代码为指令序列"""
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': '缺少代码'}), 400
    result = parse_turtle_code(data['code'])
    return jsonify(result)
