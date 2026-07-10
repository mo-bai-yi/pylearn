"""Turtle 可视化——真正执行 Python 代码，用 Mock Turtle 拦截绘图命令。

不再静态解析（无法处理循环和变量），而是直接在子进程中运行用户代码，
把 turtle 模块替换为记录命令的 mock。
"""

import subprocess
import sys
import json


def parse_turtle_code(source: str, timeout: int = 5) -> dict:
    """执行 turtle 代码并捕获绘图命令

    Args:
        source: 用户写的 turtle 代码
        timeout: 执行超时（秒）

    Returns:
        dict: {commands: [...], error: None | str}
    """
    if not source.strip():
        return {'commands': [], 'error': '代码为空'}

    # 构建 runner：用 json.dumps 安全嵌入用户代码
    code_json = json.dumps(source)

    runner = (
        'import sys,json,types\n'
        'class _M:\n'
        ' def __init__(s):s.cmds=[]\n'
        ' def forward(s,d):s.cmds.append({"cmd":"fd","args":[float(d)]})\n'
        ' def fd(s,d):s.forward(d)\n'
        ' def backward(s,d):s.cmds.append({"cmd":"bk","args":[float(d)]})\n'
        ' def bk(s,d):s.backward(d)\n'
        ' def right(s,a):s.cmds.append({"cmd":"rt","args":[float(a)]})\n'
        ' def rt(s,a):s.right(a)\n'
        ' def left(s,a):s.cmds.append({"cmd":"lt","args":[float(a)]})\n'
        ' def lt(s,a):s.left(a)\n'
        ' def penup(s):s.cmds.append({"cmd":"pu","args":[]})\n'
        ' def pu(s):s.penup()\n'
        ' def pendown(s):s.cmds.append({"cmd":"pd","args":[]})\n'
        ' def pd(s):s.pendown()\n'
        ' def pensize(s,w):s.cmds.append({"cmd":"pensize","args":[float(w)]})\n'
        ' def pencolor(s,*a):s.cmds.append({"cmd":"pencolor","args":[str(a[0])] if a else []})\n'
        ' def color(s,*a):s.pencolor(*a)\n'
        ' def goto(s,x,y=None):\n'
        '  if y is None:x,y=x[0],x[1]\n'
        '  s.cmds.append({"cmd":"goto","args":[float(x),float(y)]})\n'
        ' def circle(s,r,*a):s.cmds.append({"cmd":"circle","args":[float(r)]})\n'
        ' def seth(s,a):s.cmds.append({"cmd":"seth","args":[float(a)]})\n'
        ' def setheading(s,a):s.seth(a)\n'
        ' def speed(s,sp):pass\n'
        ' def ht(s):s.cmds.append({"cmd":"ht","args":[]})\n'
        ' def hideturtle(s):s.ht()\n'
        ' def st(s):s.cmds.append({"cmd":"st","args":[]})\n'
        ' def showturtle(s):s.st()\n'
        ' def home(s):s.cmds.append({"cmd":"home","args":[]})\n'
        ' def clear(s):s.cmds.append({"cmd":"clear","args":[]})\n'
        ' def reset(s):s.cmds.append({"cmd":"reset","args":[]})\n'
        ' def begin_fill(s):s.cmds.append({"cmd":"begin_fill","args":[]})\n'
        ' def end_fill(s):s.cmds.append({"cmd":"end_fill","args":[]})\n'
        ' def fillcolor(s,*a):s.cmds.append({"cmd":"fillcolor","args":[str(a[0])] if a else []})\n'
        ' def __getattr__(s,n):return lambda *a,**kw:None\n'
        '_m=_M()\n'
        '_t=types.ModuleType("turtle")\n'
        '_t.Turtle=lambda:_m\n'
        '_t.Screen=lambda:types.SimpleNamespace()\n'
        '_t.bgcolor=lambda *a:None\n'
        '_t.title=lambda *a:None\n'
        'for _n in["forward","fd","backward","bk","right","rt","left","lt",'
        '"penup","pu","pendown","pd","pensize","pencolor","color",'
        '"goto","setpos","setposition","circle","dot",'
        '"setheading","seth","speed","hideturtle","ht",'
        '"showturtle","st","home","clear","done","mainloop",'
        '"exitonclick","bye","update","tracer","bgcolor"]:\n'
        ' setattr(_t,_n,getattr(_m,_n,lambda *a,**kw:None))\n'
        'sys.modules["turtle"]=_t\n'
        'exec(' + code_json + ')\n'
        'print("CMDS:"+json.dumps(_m.cmds))\n'
    )

    try:
        result = subprocess.run(
            [sys.executable, '-c', runner],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        error = None
        commands = []

        # 检查 stderr 错误
        stderr = result.stderr.strip()
        if stderr:
            if 'Error' in stderr or 'Traceback' in stderr:
                lines = stderr.split('\n')
                error = next((l.strip() for l in reversed(lines) if l.strip() and 'Traceback' not in l and 'File "' not in l and 'line ' not in l), stderr[:300])
            else:
                error = stderr[:300]

        # 解析 CMDS
        if not error:
            for line in result.stdout.strip().split('\n'):
                line = line.strip()
                if line.startswith('CMDS:'):
                    try:
                        commands = json.loads(line[5:])
                    except json.JSONDecodeError:
                        error = '命令解析失败'
                    break

        if not error and result.returncode != 0 and not commands:
            error = f'进程退出码: {result.returncode}'

        return {'commands': commands, 'error': error}

    except subprocess.TimeoutExpired:
        return {'commands': [], 'error': f'⏱️ 代码执行超过 {timeout} 秒'}
    except Exception as e:
        return {'commands': [], 'error': f'执行出错: {str(e)}'}


# 预设示例
EXAMPLE_TURTLE_CODES = {
    '正方形': '''import turtle
t = turtle.Turtle()
t.speed(5)
for i in range(4):
    t.forward(100)
    t.right(90)
t.hideturtle()
''',
    '五角星': '''import turtle
t = turtle.Turtle()
t.speed(5)
for i in range(5):
    t.forward(150)
    t.right(144)
t.hideturtle()
''',
    '螺旋': '''import turtle
t = turtle.Turtle()
t.speed(10)
for i in range(1, 40):
    t.forward(i * 10)
    t.right(60)
t.hideturtle()
''',
}
