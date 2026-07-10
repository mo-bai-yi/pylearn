"""API 路由——代码执行、批改、更新"""

from flask import Blueprint, request, jsonify
from app.utils.code_runner import run_code
from app.updater import check_update, apply_update, download_new_exe, get_local_version

bp = Blueprint('api', __name__)


@bp.route('/run', methods=['POST'])
def api_run():
    """执行代码并返回结果"""
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': '缺少 code 参数'}), 400

    code = data['code']
    timeout = data.get('timeout', 5)

    result = run_code(code, timeout)
    return jsonify(result)


@bp.route('/check', methods=['POST'])
def api_check():
    """批改练习"""
    data = request.get_json()
    if not data or 'code' not in data or 'expected' not in data:
        return jsonify({'error': '缺少参数'}), 400

    code = data['code']
    expected = data['expected']

    result = run_code(code)
    if result['error']:
        return jsonify({
            'passed': False,
            'message': f"执行出错：{result['error']}",
            'stdout': result['stdout'],
            'stderr': result['stderr'],
        })

    actual = result['stdout'].strip()
    passed = actual == expected.strip()

    return jsonify({
        'passed': passed,
        'message': '✅ 通过！' if passed else f'❌ 预期输出 "{expected.strip()}"，实际输出 "{actual}"',
        'stdout': result['stdout'],
        'stderr': result['stderr'],
    })


# ===== 热更新 API =====

@bp.route('/update/check', methods=['GET'])
def api_update_check():
    """检查更新"""
    force = request.args.get('force', '0') == '1'
    return jsonify(check_update(force=force))


@bp.route('/update/apply', methods=['POST'])
def api_update_apply():
    """应用内容热更新"""
    data = request.get_json() or {}
    parts = data.get('parts', None)
    result = apply_update(parts)
    return jsonify(result)


@bp.route('/update/download-exe', methods=['POST'])
def api_download_exe():
    """下载新 exe"""
    return jsonify(download_new_exe())


@bp.route('/update/version', methods=['GET'])
def api_version():
    """本地版本"""
    return jsonify(get_local_version())
