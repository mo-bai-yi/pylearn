# 第12章：异常处理

程序运行中难免会出错——异常处理让程序遇到错误时不会崩溃，而是优雅地处理。

## 什么是异常？

```python
# 这些代码都会报错
# print(10 / 0)        # ZeroDivisionError
# int("abc")           # ValueError
# open("no_file.txt")  # FileNotFoundError
```

程序遇到未处理的异常会立即停止运行。用 `try-except` 可以捕获并处理它们。

## try-except 基本用法

```python
try:
    num = int(input("请输入一个数字："))
    result = 100 / num
    print(f"结果是：{result}")
except ValueError:
    print("❌ 输入的不是有效数字！")
except ZeroDivisionError:
    print("❌ 不能除以零！")
```

## 捕获多种异常

```python
try:
    num = int(input("请输入一个数字："))
    result = 100 / num
    print(f"结果是：{result}")
except (ValueError, ZeroDivisionError) as e:
    print(f"❌ 出错了：{e}")
```

> 💡 `as e` 可以获取异常对象，查看具体的错误信息。

## 完整的异常结构

```python
try:
    num = int(input("请输入数字："))
    print(100 / num)
except ValueError as e:
    print(f"输入错误：{e}")
except ZeroDivisionError as e:
    print(f"数学错误：{e}")
except Exception as e:
    print(f"其他错误：{e}")
else:
    print("✅ 执行成功！没有异常发生。")
finally:
    print("👋 这句话无论如何都会执行")
```

| 部分 | 作用 |
|------|------|
| `try` | 放可能出错的代码 |
| `except` | 出错时执行 |
| `else` | 没出错时执行 |
| `finally` | 不管出不出错都执行 |

## 实战：健壮的计算器

```python
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "不能除以零"
    except TypeError:
        return "请输入数字"

# 测试
print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # 不能除以零
print(safe_divide(10, "a"))  # 请输入数字
```

## 实战：安全读取文件

```python
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"文件 {filename} 不存在"
    except PermissionError:
        return f"没有权限读取 {filename}"
    except Exception as e:
        return f"读取出错：{e}"

print(read_file_safe("存在的文件.txt"))
print(read_file_safe("不存在的文件.txt"))
```

## 什么时候用异常？

✅ **应该用：**
- 文件操作（文件可能不存在、权限不足）
- 网络请求（连接可能超时）
- 用户输入（格式可能不对）
- 类型转换（可能无效）

❌ **不用：**
- 可以用 `if` 提前判断的情况
- 正常流程控制

```python
# ✅ 好的：用 try
try:
    num = int(input("输入数字："))
except ValueError:
    print("无效输入")

# ✅ 更好的：先判断（如果简单的话）
user_input = input("输入数字：")
if user_input.isdigit():
    num = int(user_input)
else:
    print("无效输入")
```

## 试试看

写一个程序，让用户输入两个数字并做除法，用异常处理所有可能的错误情况。
