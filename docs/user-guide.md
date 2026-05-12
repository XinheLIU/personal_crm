# Compass — 用户手册

*Last updated: 2026-05-12.*

Compass 是一个本地个人 CRM，追踪你在追求的所有目标（公司、项目、人）、每一次有意义的互动，并把这些信号迭代到你的个人 profile 中。

**技术栈：** SQLite + Markdown，Claude Code / OpenCode 作为运行时。无需服务器，无需云端，无需登录。备份 = `git push`。

**核心习惯：** 每次有意义的互动之后，执行一次 `compass track`。

---

## 1. 安装与初始化

### 1.1 初始化系统

```bash
cd ~/compass  # 或 ~/personal-crm
uv run python crm.py init
```

这一步会创建：
- `crm.db` — SQLite 数据库
- `data/journal/`、`data/targets/`、`data/assets/`、`data/retros/` — 目录
- `north_star.md` 和 `profile.md` — 种子文件

### 1.2 注入冷启动数据（推荐）

冷启动数据独立存储在 `data/seed.sql`，可读、可修改、可直接用 SQLite 执行。注入后 Analyzer 和 Strategist 立刻有内容可分析，无需等待真实数据积累。

**方式一 — 通过 CLI（推荐）：**
```bash
uv run python crm.py seed
```

**方式二 — 直接用 SQLite（无需 Python）：**
```bash
sqlite3 crm.db < data/seed.sql
```

写入内容：4 个 targets、5 个 lanes、10 条真实感的 touchpoints，涵盖求职、自媒体、社区三类场景。

**包含数据预览：**

| Target | Kind | Tier | Lane | Stage |
|---|---|---|---|---|
| 字节跳动 | job | dream | L7 Staff Engineer (Go) | interview |
| 字节跳动 | job | dream | L6 Senior Engineer (Go) | applied |
| Hugging Face | job | strong | ML Engineer | open |
| My Blog | media | try | Static Analysis Series | closed |
| 朋友们 | community | try | Coffee Chats Network | open |

### 1.3 填写 north_star 和 profile

`north_star.md` — 季度方向（由人填写，驱动 Strategist 的优先级判断）：

```
## This quarter's goals (1-3)
1. [你正在追求的目标]
2. [目标]
3. [目标]

## Success criteria
- [怎么算有进展？]

## NOT chasing right now
- [明确搁置的方向]
```

`profile.md` — 个人 proposition（由人 + Strategist 迭代填写）：

```
## Who I am
[你当前的角色、方向、给世界的价值]

## Core skills
- [技能]
- [技能]

## Next-stage goals
[你在建立什么——由市场反馈迭代]
```

### 1.4 把 `compass` 加入 $PATH

```bash
# 方式 A：符号链接到 ~/bin
mkdir -p ~/bin
ln -s "$(pwd)/crm.py" ~/bin/compass
chmod +x ~/bin/compass
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 方式 B：alias（加到 ~/.zshrc 或 ~/.bashrc）
alias compass='uv run python3 /path/to/compass/crm.py'
```

验证：

```bash
compass --help
```

---

## 2. 日常使用 — `/track`

### 2.1 核心命令

每次有意义的互动后：

```bash
compass track "收到了字节跳动 HR 的三面邀请，定在周五下午 3 点"
```

`compass track` 永远做两件事：

1. **先把原文写入** `data/journal/<yyyy-mm-dd>.md` — 即使 DB 写入失败，journal 也安全。
2. **提示你在 Claude Code / OpenCode 里运行 `/track`**，完成结构化解析。

### 2.2 在 Claude Code / OpenCode 里完成解析

CLI 打印提示后，在 AI IDE 中执行：

```
/track 收到了字节跳动 HR 的三面邀请，定在周五下午 3 点
```

Tracker agent 会：
- 匹配或新建 **target**（如"字节跳动"，kind: job）
- 匹配或新建 **lane**（如"L7 Staff Engineer (Go)"，kind: job_app）
- 追加 **touchpoint**，自动检测 stage 推进（如"三面邀请" → stage: interview）
- 提取 `summary`、`insights`、`next_step`

### 2.3 哪些值得 track？

只要动了脑筋、涉及另一个人的，都值得：
- 发出了申请、提案、pitch
- 打了电话、约了会面
- 发了或收到了包含决定/承诺的消息
- 发布了博客、repo、tweet
- 收到了回复或拒绝
- 和某个人的重要对话

**不需要 track：** 随机想法、内部规划、纯个人思考。

### 2.4 `/track` 的边界

- ❌ 不会生成计划或建议 — 这是 Analyzer / Strategist 的职责
- ❌ 不会评价互动的价值
- ❌ 不会修改过去的 touchpoint — append-only
- ❌ 不会为新 target 选择 tier — 永远默认为 `try`，人工决策
- ✅ 即便 LLM 不可用，journal 写入仍然成功

---

## 3. 目标分析 — `/analyze`

想深入了解和某个 target 的关系现状时：

### 3.1 找到 target ID

```bash
compass sql "SELECT id, name, kind, tier FROM target WHERE status = 'active';"
```

### 3.2 查看时间线

```bash
compass analyze <target_id>
```

输出该 target 所有 lanes、所有 touchpoints 的原始时间线。

### 3.3 获取 AI 综合分析

在 Claude Code / OpenCode 中：

```
/analyze <target_id>
```

Analyzer 会：
- 加载该 target 的完整关系图（lanes、touchpoints、linked assets、north_star 上下文）
- 输出：上次有意义互动是哪天、承诺了什么、哪些已逾期、下一步建议
- 结合你的 `north_star.md` 判断优先级

---

## 4. 周期性复盘 — `/review`

在里程碑或周期结束时运行（每周、双周，或任意你觉得该复盘的时候）：

### 4.1 查看原始数据

```bash
compass review
```

输出：所有 open lanes + 最近 20 条 touchpoints。

### 4.2 获取 AI 复盘摘要

在 Claude Code / OpenCode 中：

```
/review
```

Strategist 会：
1. 拉取近期 touchpoints 和 open lanes
2. 读取 `north_star.md` 和 `profile.md`
3. 对最热的 N 个 target 运行 `/analyze`
4. 综合输出 **retro_brief**：≤5 条行动建议、≤8 个半天，优先级与 north_star 对齐
5. 提取市场反馈，更新 `profile.md` 建议（如"字节跳动看重 Go 底层能力 — 更新简历"）
6. 写入 `data/retros/<iso>.md`，向 `retro_brief` 表追加一行

**retro_brief 是 append-only 的。** 历史记录永远不被修改或删除——不认可旧的，就在新的一次里纠正。

---

## 5. 数据模型速查

### Target

| 字段 | 可选值 |
|---|---|
| `kind` | job, media, community, collaborator |
| `tier` | dream, strong, try, cold |
| `status` | active, dormant, closed |

### Lane

| 字段 | 可选值 |
|---|---|
| `kind` | job_app, content, event, outreach |
| `stage` | open, applied, screening, interview, offer, rejected, closed |

### Touchpoint

| 字段 | 可选值 |
|---|---|
| `kind` | applied, call, message, post, meet, reply |

---

## 6. 直接 SQL 查询

无需 LLM，直接读数据库：

```bash
# 列出所有活跃 target
compass sql "SELECT name, kind, tier, status FROM target WHERE status = 'active';"

# 所有 open lanes
compass sql "SELECT l.title, t.name, l.stage FROM lane l JOIN target t ON l.target_id = t.id WHERE l.status = 'active';"

# 最近 10 条 touchpoints
compass sql "SELECT tp.happened_at, tp.kind, tp.summary, l.title, t.name FROM touchpoint tp JOIN lane l ON tp.lane_id = l.id JOIN target t ON l.target_id = t.id ORDER BY tp.happened_at DESC LIMIT 10;"

# 查看某 target 的详细时间线
compass analyze <target_id>
```

---

## 7. 目录结构

```
~/compass/
├── crm.db                      # SQLite 数据库（gitignored）
├── schema.sql                  # 幂等 schema
├── north_star.md               # 季度目标（手动填写）
├── profile.md                  # 个人 proposition（人 + Strategist 迭代）
├── crm.py                      # CLI 入口
├── prompts/
│   ├── tracker.md              # /track 解析规则
│   ├── analyzer.md            # /analyze prompt
│   └── strategist.md          # /review prompt
└── data/
    ├── journal/<yyyy-mm-dd>.md # 每日原始日志
    ├── targets/<id>/notes.md  # 每个 target 的自由笔记
    ├── assets/                 # 资产文件
    └── retros/<iso>.md         # 复盘摘要
```

---

## 8. 设计原则

- **先记录，再整理。** 唯一必须的 habit 是 `compass track`。系统靠零其他操作也能长期有用。
- **过去不可改，未来可以变。** Touchpoints 和 retro_briefs append-only —— 可信赖的历史。新数据反映新判断。
- **优雅降级。** LLM 挂了？`compass track` 依然写 journal。恢复 = 之后对着 journal 重新跑 `/track`。
- **偏见即策略。** 优先级顺序存在于 `prompts/strategist.md` 一行。生命转折时，10 秒翻转，无需改代码。
- **系统自证其复杂度。** 新 agent / 新表 / 新列，只在 retro_brief 明确指出其缺失时才能添加。
- **备份 = git push。** 整个状态都在这个目录里。

---

## 9. 命令速查

| 命令 | 作用 |
|---|---|
| `compass init` | 初始化数据库和目录 |
| `compass seed` | 注入冷启动演示数据 |
| `compass track "..."` | 记录一条 interaction |
| `compass analyze <id>` | 查看某个 target 的完整时间线 |
| `compass review` | 查看所有 open lanes + 最近 touchpoints |
| `compass sql "SELECT ..."` | 直接读 SQL |
| `compass migrate` | 重新应用 schema.sql（幂等） |

---

## 10. 故障排除

### "No database yet. Run `compass init` first."
```bash
compass init
```

### command not found 或 Permission denied
```bash
echo $PATH   # 确认 ~/bin 在 PATH 中
compass --help  # 验证符号链接有效
```

### 数据库 schema 漂移
```bash
compass migrate
```

### 想清空重来？
```bash
rm crm.db
compass init
compass seed   # 重新注入冷启动数据
```
