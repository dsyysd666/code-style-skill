# 四套预设风格：完整规则表

给出对照选项时按本表执行。用户选定某套后，把对应规则抄进档案文件（用户级 `~/.workbuddy/skill-data/code-style-skill/profile.md`，不是 skill 包内的模板）。

> **配置开关优先级**：`style-profile.template.md` 里有两个开关——调试打印强度（verbose/standard/off）和语法自由度（strict/relaxed）。它们会**覆盖**本表的默认行为：
> - `off` / `standard`：本表 D 型"每步打印日志"要相应减弱为只在关键节点或报错处打印。
> - `relaxed`：本表 A/B/D 里的"禁用语法"（三元、推导式、lambda）不再硬性禁止，只保留用户列入"硬规矩"的禁用项。
> 生成代码前先读档案的这两个开关，再对照本表，避免规则打架导致代码膨胀或日志噪音。

---

## A 新手友好型

**性格**：读完不用回头想，啰嗦但安全。适合刚学、或想在出错时逐行核对的人。

| 维度 | 规则 |
|---|---|
| 变量命名 | 完整英文单词或词组，`average_score` 而非 `avg`；宁长不缩写 |
| 函数命名 | `动词_名词`，如 `calculate_average` |
| 一行几件事 | 严格一件。不链式调用，不复合表达式 |
| 中间变量 | 每个步骤都单独存成变量，哪怕只用一次 |
| 注释密度 | 每行或每两行一条，说明"这一步在做什么" |
| 语法限制 | 不用三元、推导式、lambda、解包、装饰器、递归 |
| 嵌套 | 最多两层，`if` 提前 return 代替深层嵌套 |
| 排查 | 每个中间结果都打印；每步前有 `# 第 N 步` 编号注释 |
| 报错 | `print(f"第2步出错：scores 的值是 {scores}，应该是数字列表")` |

**样例感受**：
```python
# 第 1 步：准备数据
numbers = [12, 5, 8, 20, 3]

# 第 2 步：求总和
total = 0
for number in numbers:
    total = total + number

# 第 3 步：求平均
average = total / len(numbers)
print("平均值是", average)
```

---

## B 紧凑型

**性格**：短、快、信息密度高。适合已经很熟、看惯了短写法的人。

| 维度 | 规则 |
|---|---|
| 变量命名 | 短名，`n` `xs` `res` `i`；作用域小就用单字母 |
| 函数命名 | 短动词，`avg()` `fmt()` |
| 一行几件事 | 允许链式、允许复合表达式 |
| 中间变量 | 能省就省，只在复用超过两次时才存 |
| 注释密度 | 只在"为什么这么写"不显然的地方写 |
| 语法限制 | 放开：推导式、三元、解包、lambda 均可用 |
| 嵌套 | 不设限，以读得顺为准 |
| 排查 | 只在关键出口打印一次；出错靠读栈 |
| 报错 | 简短，`raise ValueError("empty input")` |

**样例感受**：
```python
nums = [12, 5, 8, 20, 3]
avg = sum(nums) / len(nums)
print(avg, [n for n in nums if n > avg])
```

---

## C 工程型

**性格**：像正式项目里的代码。适合要给别人看、要长期维护的场景。

| 维度 | 规则 |
|---|---|
| 变量命名 | 完整语义名，避免泛词 `data` `res` |
| 函数命名 | `动词_名词`，单一职责 |
| 类型标注 | 全部参数和返回值都要标注 |
| 文档字符串 | 每个函数一段，写明参数、返回、可能抛出的异常 |
| 结构 | 入口函数 + 若干小函数，主流程不超过 10 行 |
| 异常处理 | 不裸 `except`；捕获具体异常；自定义业务异常 |
| 注释密度 | 只写"为什么"，不写"是什么"（代码自己说明是什么） |
| 排查 | 用 logging 模块，分 INFO / DEBUG / ERROR 级别 |
| 报错 | 带上下文，`raise ValueError(f"scores 为空，无法计算均值")` |

**样例感受**：
```python
import logging
from typing import Sequence

logger = logging.getLogger(__name__)

def calculate_average(scores: Sequence[float]) -> float:
    """计算一组分数的算术平均值。

    Args:
        scores: 分数序列，不能为空。

    Returns:
        平均值。

    Raises:
        ValueError: scores 为空时。
    """
    if not scores:
        raise ValueError("scores 为空，无法计算均值")
    logger.debug("计算平均值，样本量=%d", len(scores))
    return sum(scores) / len(scores)
```

---

## D 防御型

**性格**：步步设防，出错一定有交代。适合线上排查痛苦过的人。

| 维度 | 规则 |
|---|---|
| 参数校验 | 每个函数入口先校验类型、范围、空值 |
| 日志 | 每个步骤前后各一条日志，带变量值 |
| 异常处理 | 每步单独 try，出错时记录现场并给可操作提示 |
| 中间变量 | 全部保留，便于打印和断点 |
| 注释密度 | 每步一条，注明"这一步可能因为什么失败" |
| 报错信息 | 固定三段式：哪一步 / 当前值是什么 / 期望什么 / 建议怎么改 |
| 返回值 | 不加修饰地返回，不吞异常 |

**样例感受**：
```python
def calculate_average(scores):
    # 第 1 步：校验入参 —— 可能失败原因：传了 None 或空列表
    if scores is None:
        print("[出错] 第1步：scores 是 None，期望是数字列表。请检查上游赋值。")
        return None
    if len(scores) == 0:
        print("[出错] 第1步：scores 是空列表，无法求平均。请先确认数据来源。")
        return None

    # 第 2 步：求和 —— 可能失败原因：元素不是数字
    try:
        total = sum(scores)
    except TypeError as e:
        print(f"[出错] 第2步：scores 里有非数字元素 {scores}，原错误：{e}")
        return None

    # 第 3 步：求平均
    average = total / len(scores)
    print(f"[完成] 共 {len(scores)} 个数，平均值 {average}")
    return average
```

---

## 混着来：常见组合

用户说"我要混着来"时，按下面的组合抄规则：

| 组合 | 适用 |
|---|---|
| A 的命名 + D 的排查 | 最推荐新手：看得懂，出错也有交代 |
| B 的简洁 + C 的类型标注 | 熟手写小工具 |
| C 的结构 + A 的注释密度 | 要交作业、要给人看 |
| A 的一行一件事 + D 的三段式报错 | 纯自学、打算逐行 debug |
