# 第6章：循环

循环让计算机做**重复的事情**——这正是计算机最擅长的地方。

## for 循环

`for` 循环用来**遍历**一个序列（比如列表、字符串）：

```python
# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢吃 {fruit}")

# 遍历字符串
for ch in "Python":
    print(ch)
```

## range() 函数

`range()` 生成一个整数序列，经常和 for 循环配合使用：

```python
# range(5) → 0, 1, 2, 3, 4
for i in range(5):
    print(i)  # 打印 0 到 4

# range(2, 7) → 2, 3, 4, 5, 6
for i in range(2, 7):
    print(i)

# range(1, 10, 2) → 1, 3, 5, 7, 9（步长为2）
for i in range(1, 10, 2):
    print(i)
```

## while 循环

`while` 循环在条件为真时持续执行：

```python
count = 0
while count < 5:
    print(f"第 {count + 1} 次")
    count += 1  # 别忘了更新条件！

print("循环结束")
```

> ⚠️ **死循环**：如果条件永远为真，循环会一直运行！记得在循环里更新条件。

## break 和 continue

```python
# break — 跳出整个循环
for i in range(10):
    if i == 5:
        break   # 到5就停止
    print(i)    # 输出：0 1 2 3 4

# continue — 跳过当前次，继续下一次
for i in range(5):
    if i == 2:
        continue  # 跳过2
    print(i)      # 输出：0 1 3 4
```

## 实用例子：累加求和

```python
# 计算 1 到 100 的和
total = 0
for i in range(1, 101):
    total += i
print(f"1到100的和是：{total}")
```

## 试试看

试着在右侧编辑器里写一个循环，打印出你的5个爱好！
