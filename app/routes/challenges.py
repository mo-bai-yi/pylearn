"""闯关模块路由"""

from flask import Blueprint, render_template, jsonify, request
from app.db import get_db
from app.utils.code_runner import run_code
import os
import glob
import yaml

bp = Blueprint('challenges', __name__, url_prefix='/challenges')

from app.path_utils import get_content_dir
CHALLENGES_DIR = get_content_dir('challenges')


def _load_challenges():
    """加载所有关卡定义"""
    challenges = []
    files = sorted(glob.glob(os.path.join(CHALLENGES_DIR, '*.yaml')))
    for i, f in enumerate(files):
        name = os.path.basename(f).replace('.yaml', '')
        # 从文件名提取标题
        parts = name.split('-', 1)
        title = parts[1].replace('-', ' ').title() if len(parts) > 1 else name
        challenges.append({
            'id': name,
            'title': title,
            'file': f,
            'index': i,
        })
    return challenges


@bp.route('/')
def challenge_list():
    challenges = _load_challenges()
    # 获取闯关进度
    db = get_db()
    progress = {}
    for row in db.execute('SELECT * FROM challenge_progress').fetchall():
        progress[row['challenge_id']] = dict(row)

    return render_template('challenges/list.html',
                           title='编程闯关',
                           challenges=challenges,
                           progress=progress)


@bp.route('/play/<challenge_id>')
def challenge_play(challenge_id):
    challenges = _load_challenges()
    chal = None
    for c in challenges:
        if c['id'] == challenge_id:
            chal = c
            break
    if not chal:
        return '关卡不存在', 404

    # 用 PyYAML 解析关卡文件
    with open(chal['file'], 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    chal['title'] = data.get('title', chal['title'])
    description = data.get('description', '')
    initial_code = data.get('initial_code', '# 请在此编写代码\npass')
    test_cases = data.get('tests', [])

    return render_template('challenges/play.html',
                           title=chal['title'],
                           challenge=chal,
                           description=description.strip(),
                           initial_code=initial_code.strip(),
                           test_cases=test_cases)


@bp.route('/api/submit', methods=['POST'])
def challenge_submit():
    """提交闯关答案"""
    data = request.get_json()
    code = data.get('code', '')
    challenge_id = data.get('challenge_id', '')

    # 运行代码
    result = run_code(code)
    if result['error']:
        return jsonify({'passed': False, 'message': result['error']})

    # 记录尝试
    db = get_db()
    row = db.execute('SELECT * FROM challenge_progress WHERE challenge_id = ?',
                     (challenge_id,)).fetchone()
    attempts = row['attempts'] + 1 if row else 1

    if row:
        db.execute('UPDATE challenge_progress SET attempts = ?, last_result = ? WHERE challenge_id = ?',
                   (attempts, result['stdout'][:500], challenge_id))
    else:
        db.execute('INSERT INTO challenge_progress (challenge_id, attempts, last_result) VALUES (?, ?, ?)',
                   (challenge_id, attempts, result['stdout'][:500]))
    db.commit()

    return jsonify({
        'passed': True,
        'message': '代码已提交！',
        'stdout': result['stdout'],
        'stderr': result['stderr'],
    })
