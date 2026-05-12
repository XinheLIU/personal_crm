# Compass — 快速上手

*Last updated: 2026-05-12.*

5 分钟跑起来，体验完整的 Analyzer + Strategist 能力。

---

## Step 1 — 初始化（30 秒）

```bash
cd ~/compass   # 或 ~/personal-crm
uv run python crm.py init
```

输出：

```
compass init complete.
  DB:       /path/to/crm.db
  Journal:  /path/to/data/journal
  North Star: /path/to/north_star.md
  Profile:  /path/to/profile.md
```

---

## Step 2 — 注入冷启动数据（10 秒）

### 冷启动数据

冷启动数据独立存储在 `data/seed.sql`，可读、可修改、可直接用 SQLite 执行。

**方式一 — 通过 CLI（推荐）：**
```bash
uv run python crm.py seed
```

**方式二 — 直接用 SQLite（无需 Python）：**
```bash
sqlite3 crm.db < data/seed.sql
```

写入内容：4 个 targets、5 个 lanes、10 条真实感的 touchpoints，涵盖求职、自媒体、社区三类场景。

| Target | Kind | Tier | Lane | Stage |
|---|---|---|---|---|
| 字节跳动 | job | dream | L7 Staff Engineer (Go) | interview |
| 字节跳动 | job | dream | L6 Senior Engineer (Go) | applied |
| Hugging Face | job | strong | ML Engineer | open |
| My Blog | media | try | Static Analysis Series | closed |
| 朋友们 | community | try | Coffee Chats Network | open |

```
Cold-start data seeded. Run `compass review` or /analyze on any target to see it in action.
```

---

## Step 3 — 把 `compass` 丢到 $PATH（可选，但推荐）

```bash
# macOS/Linux
mkdir -p ~/bin
ln -s "$(pwd)/crm.py" ~/bin/compass
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

以后就可以直接打 `compass review` 而不是 `uv run python crm.py review`。

---

## Step 4 — 立刻体验 `/analyze`

在 Claude Code 或 OpenCode 里：

```
/analyze target_bdy
```

你会看到字节跳动 L7 面试的完整时间线：
- 猎头对接 → 电话了解 → 正式投递 → 一面算法 → 二面系统设计/项目 → 三面待定

以及每条 touchpoint 的 insights 和 next_step。

---

## Step 5 — 立刻体验 `/review`

```
/review
```

Strategist 会：
1. 拉取所有 open lanes（字节 L7/L6 面试中、Hugging Face 开放中、朋友们 Coffee Chats）
2. 拉取最近 20 条 touchpoints
3. 运行 `/analyze` 在最热的 targets 上
4. 结合 `north_star.md` 和 `profile.md` 给出 ≤5 条行动建议

---

## 日常使用

从此每天只需要记住一个动作：

```bash
# 记录任何有意义的 interaction
compass track "收到了字节跳动的三面邀请，定在周五下午"
```

然后在 Claude Code / OpenCode 里：

```
/track 收到了字节跳动的三面邀请，定在周五下午
```

Tracker 会自动解析这条句子，更新 lane stage，追加 touchpoint。

---

## 命令速查

| 命令 | 作用 |
|---|---|
| `compass init` | 初始化数据库和目录 |
| `compass seed` | 注入冷启动演示数据 |
| `compass track "..."` | 记录一条 interaction |
| `compass analyze <id>` | 查看某个 target 的完整时间线 |
| `compass review` | 查看所有 open lanes + 最近 touchpoints |
| `compass sql "SELECT ..."` | 直接查 SQL |

---

## 下一步

- 填写真实的 `north_star.md`（季度目标）和 `profile.md`（你是谁、你会什么）
- 用 `compass review` 驱动周期性复盘
- 随着数据积累，Analyzer 的建议会越来越精准
