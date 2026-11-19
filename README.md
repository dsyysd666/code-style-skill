# 个人代码风格 Skill（code-style-skill）

> 让 AI 写出的代码，读起来像你自己写的。

一个用于 AI 编程助手（如 WorkBuddy / Claude / Cursor 等）的 Skill。它通过一次 5 分钟的风格校准，建立你的**个人代码风格档案**，之后 AI 生成的所有代码都严格按这个档案执行——命名、注释、结构、排查方式都按你的习惯来，出错时你能一眼定位。

## English

A skill that makes AI-generated code read like **you** wrote it. It calibrates your personal code style once (5 minutes), saves a profile, then enforces it on every code generation: naming, comments, structure, and debuggability all match your habits.

---

## 它解决什么问题

AI 写的代码常常"能跑但不是我的写法"：命名陌生、结构绕、没有注释，一旦出错根本不知道从哪查起。

本 Skill 的核心理念：**风格不是形容词，是一组能被逐条检查的规则。**
"简洁一点" AI 没法执行；"变量名用完整英文单词、每个 if 后面写注释说明判断什么"才能执行。

它做的事：

1. **风格校准**：出一道 10 行内的小题，用同一道题给出 4 种风格（新手友好 / 紧凑 / 工程 / 防御）供你挑选，也支持直接贴 20 行你写过的代码自动提取风格。
2. **翻译成规则**：把你说的"看得懂""出错知道在哪"翻译成可检查的命名、注释、排查规则。
3. **按风格生成**：每次写代码前复述规则，代码中附"排查地图"，代码后附动态自查表。
4. **档案可迁移**：档案存在你自己的目录，可导出备份、导入恢复，不随 Skill 包发布。

## 快速开始

### 安装

把本目录（`code-style-skill-v2`，可重命名为 `code-style-skill`）复制到你的 Agent 的 skills 目录，例如：

```
# WorkBuddy 用户级技能目录
~/.workbuddy/skills/code-style-skill/
```

复制后应包含这些文件：

```
code-style-skill/
├── SKILL.md                        # 主指令（Agent 读取这个）
├── README.md                       # 本文件
├── LICENSE / CHANGELOG.md / CONTRIBUTING.md / .gitignore
├── assets/
│   └── style-profile.template.md   # 空白档案模板（只读）
├── references/
│   ├── profile-management.md       # 档案存放与导入导出规范
│   ├── style-presets.md            # 四套预设风格规则表
│   └── style-checklist.md          # 风格维度清单
└── examples/                       # 生成结果示例
```

### 第一次使用

对 Agent 说一句"按我的风格写代码"或 "write code in my style" 即可触发。它会：

1. 发现你还没有档案 → 进入校准
2. 出一道小题 → 展示 4 种风格 → 你选一个打底，说几个硬规矩和最怕的写法
3. 把你的偏好翻译成规则，写入档案（默认 `~/.workbuddy/skill-data/code-style-skill/profile.md`）
4. 用选定风格把那道题重写一遍给你确认

> 提示：如果你手上有自己写过的代码，直接贴 20 行给它，比出题更快更准。

### 日常使用

档案建好后，直接说需求即可，开头会自动复述一行"按你的风格：……"让你确认。常用指令：

| 你说 | 效果 |
|---|---|
| 按我的风格写个 XX | 按档案生成代码 |
| 调试打印改成 off | 只改配置开关那一条，回显新旧对比 |
| 语法放宽一点 | strict → relaxed，允许 lambda / 推导式 |
| 导出我的风格档案 | 备份到 `~/Downloads/code-style-profile.md` |
| 从 XX 导入风格档案 | 恢复档案（导入前自动备份旧档案） |
| 换个风格 / 看看我的风格档案 | 列出或切换档案 |
| 这段随便写，不用管风格 | 临时放开（会声明"这段未按你的风格"） |

## 核心设计

### 两个配置开关

| 开关 | 取值 | 含义 |
|---|---|---|
| 调试打印强度 | `verbose` / `standard`（默认）/ `off` | 控制打印量：每步+变量 / 关键节点 / 只在报错 |
| 语法自由度 | `strict`（默认）/ `relaxed` | 是否允许 lambda、推导式等语法糖（硬规矩仍禁） |

### 档案与隐私

**个人档案不放在 Skill 包里**，这是有意设计：

- 分享 / 上传本仓库不会泄露你的私人风格偏好
- 更新 Skill 不会覆盖你的档案
- 同一个 Skill 可支持多项目不同风格

档案位置（详见 `references/profile-management.md`）：

| 类型 | 路径 |
|---|---|
| 用户档案（默认） | `~/.workbuddy/skill-data/code-style-skill/profile.md` |
| 项目档案 | `<项目根>/.workbuddy/code-style-profile.md` |
| 命名档案 | `~/.workbuddy/skill-data/code-style-skill/profiles/<名字>.md` |

查找顺序：项目档案 → 用户档案 → 无档案（触发校准）。

> 非 WorkBuddy 环境：把上述路径改成一个你有写权限的目录即可（改 `references/profile-management.md`）。

### 触发词

中文：代码风格、按我的风格写、统一代码风格、我想让代码像我写的、定义我的编码习惯、生成我看得懂的代码

English: code style, my coding style, match my coding style, write code in my style, keep a personal code style profile

## 示例

`examples/` 下有同一道题、不同配置生成的真实代码：

- `gen_standard_strict.py` — standard 打印 + strict 语法（手写排序，54 行）
- `gen_off_relaxed.py` — off 打印 + relaxed 语法（推导式 / lambda，32 行）
- `first_use_demo.py` — 首次校准后生成的接口代码（C 工程型）

三者功能输出一致，直观展示配置开关对代码风格的影响。

## 边界

- 只管**写法**，不保证功能正确性（功能问题正常排查）
- 档案含个人偏好，导出 / 分享前会向你确认，不会主动上传外部服务
- 无档案又急着要代码时，先用新手友好型出代码，结尾提醒是否校准

## 贡献与许可

欢迎贡献，见 [CONTRIBUTING.md](CONTRIBUTING.md)。本项目采用 [MIT License](LICENSE)，可自由使用、修改、商用，只需保留署名。

---

**English summary**: A code-style calibration skill for AI coding assistants. It asks one small question, shows four style variants, translates your preferences into checkable rules, saves your profile outside the skill package, and enforces it on all future code generation with debugging maps and dynamic checklists. MIT licensed.
