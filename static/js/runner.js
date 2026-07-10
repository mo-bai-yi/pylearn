/* 代码运行交互 (playground 页面) */

async function runCode() {
    if (!playgroundEditor) return;

    const output = document.getElementById('output');
    output.className = 'output-area';
    output.textContent = '⏳ 正在运行代码...';

    const code = playgroundEditor.getValue();

    try {
        const resp = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, timeout: 5 })
        });
        const data = await resp.json();

        let html = '';
        if (data.stdout) {
            html += escHtml(data.stdout);
        }
        if (data.stderr) {
            html += '<div class="stderr">' + escHtml(data.stderr) + '</div>';
        }
        if (data.error) {
            html += '<div class="error-msg">' + escHtml(data.error) + '</div>';
        }
        if (!html) {
            html = '✅ 执行完成（无输出）';
        }
        output.innerHTML = html;
    } catch (err) {
        output.innerHTML = '<div class="error-msg">❌ 请求失败：' + escHtml(err.message) + '</div>';
    }
}

function resetCode() {
    if (!playgroundEditor) return;
    playgroundEditor.setValue(`# 欢迎来到 Pylearn 代码演示台！
# 在这里编写你的 Python 代码，然后点击"运行"

print("Hello, 世界！")

# 试试计算
a = 42
b = 7
print(f"{a} + {b} = {a + b}")
print(f"{a} × {b} = {a * b}")

# 试试列表
fruits = ["苹果", "香蕉", "橙子"]
for f in fruits:
    print(f"我喜欢吃 {f}")
`);
    clearOutput();
}

function clearOutput() {
    const output = document.getElementById('output');
    output.className = 'output-area empty';
    output.textContent = '点击「运行」查看代码输出...';
}
