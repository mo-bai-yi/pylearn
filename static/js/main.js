/* Pylearn 通用脚本 */

// 工具：HTML 转义
function escHtml(s) {
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}

// 工具：获取当前时间戳
function now() {
    return new Date().toISOString();
}
