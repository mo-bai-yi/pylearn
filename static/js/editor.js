/* 代码编辑器初始化 (CodeMirror 5) */

let playgroundEditor = null;

document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('code-editor');
    if (!textarea) return;

    playgroundEditor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        theme: 'material-darker',
        autoCloseBrackets: true,
        matchBrackets: true,
        extraKeys: {
            'Ctrl-Enter': function(cm) { runCode(); },
            'Cmd-Enter': function(cm) { runCode(); },
        }
    });

    // 自适应高度
    playgroundEditor.setSize(null, '100%');
});

// 页面关闭前调整编辑器
window.addEventListener('resize', function() {
    if (playgroundEditor) {
        playgroundEditor.refresh();
    }
});
