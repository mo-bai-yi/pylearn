"""Pylearn - Python 自学平台

两种启动模式：
  python run.py          → 桌面窗口模式（首选，需 pywebview）
  python run.py --browser → 浏览器模式（开发测试用）

打包 exe 后双击自动进入桌面窗口模式。
"""

import sys
import os
import threading
from app import create_app

app = create_app()
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000


def start_flask():
    """后台启动 Flask"""
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, use_reloader=False)


def mode_browser():
    """浏览器模式——自动打开浏览器"""
    import webbrowser
    url = f'http://{FLASK_HOST}:{FLASK_PORT}'
    print(f"""
╔═══════════════════════════════════════════╗
║  Pylearn - Python 互动自学平台            ║
║                                           ║
║  浏览器模式 · 已自动打开 {url}  ║
║  关闭此窗口即可停止                        ║
╚═══════════════════════════════════════════╝
    """)
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()


def mode_desktop():
    """桌面窗口模式——原生窗口，无需浏览器"""
    import webview
    url = f'http://{FLASK_HOST}:{FLASK_PORT}'

    # 确保 Flask 已启动
    import time
    time.sleep(1)

    print("""
╔═══════════════════════════════════════════╗
║  Pylearn - Python 互动自学平台            ║
║                                           ║
║  桌面模式 · 关闭窗口即可退出              ║
╚═══════════════════════════════════════════╝
    """)

    window = webview.create_window(
        title='Pylearn - 学 Python，从这里开始',
        url=url,
        width=1200,
        height=800,
        resizable=True,
        min_size=(900, 600),
    )
    webview.start()  # ← 必须调用 start() 才会显示窗口


if __name__ == '__main__':
    # 启动 Flask（后台 daemon 线程）
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    # --browser 参数 → 强制浏览器模式
    if '--browser' in sys.argv:
        mode_browser()
        # 浏览器模式需要保持主线程活着
        try:
            t.join()
        except KeyboardInterrupt:
            print("\n程序已退出")
        sys.exit(0)

    # 默认走桌面模式
    try:
        mode_desktop()
    except Exception as e:
        print(f"\n⚠️ 桌面模式不可用: {e}")
        print("   自动切换到浏览器模式\n")
        mode_browser()
        try:
            t.join()
        except KeyboardInterrupt:
            print("\n程序已退出")
