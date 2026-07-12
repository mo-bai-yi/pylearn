# 🐍 Pylearn - Python 互动自学平台

零基础友好的 Python 交互式学习工具，打开浏览器就能学！

## 功能

| 模块 | 说明 |
|------|------|
| 📖 **互动教程** | 从 Hello World 到函数，每课配有可运行的代码示例 |
| 🎮 **编程闯关** | 通过编程挑战检验学习成果，自动判题 |
| 💻 **代码演示台** | 自由编写和运行 Python 代码，实时看结果 |
| 🐢 **Turtle 画板** | 用代码画画，直观理解循环和函数的执行过程 |

## 快速开始

```bash
# 1. 安装依赖
pip install flask

# 2. 启动
python run.py

# 3. 打开浏览器
# → http://127.0.0.1:5000
```

## 项目结构

```
pylearn/
├── run.py                  # 启动入口
├── app/
│   ├── routes/             # 页面路由
│   │   ├── main.py         # 首页
│   │   ├── lessons.py      # 教程
│   │   ├── challenges.py   # 闯关
│   │   ├── playground.py   # 演示台
│   │   ├── api.py          # 代码执行 API
│   │   └── turtle.py       # Turtle 画板
│   └── utils/
│       ├── code_runner.py  # 安全代码执行
│       ├── content_loader.py # 教程内容加载
│       └── turtle_viz.py   # Turtle 命令解析
├── content/
│   ├── lessons/            # 教程 Markdown
│   └── challenges/         # 闯关定义 (YAML)
├── templates/              # HTML 模板
└── static/                 # CSS/JS
```

## 教程目录

1. Hello, World!
2. 变量
3. 字符串
4. 数字和运算
5. 条件判断
6. 循环
7. 列表
8. 函数

## 安全说明

代码演示台在受限的子进程中运行用户代码，有以下安全限制：
- 禁用危险模块：os, subprocess, shutil, ctypes, socket 等
- 禁用 eval/exec/open 等危险内置函数
- 5 秒执行超时自动终止
