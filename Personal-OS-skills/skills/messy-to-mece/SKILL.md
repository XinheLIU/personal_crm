---
name: messy-to-mece
description: Distill a messy markdown notes file (流水反思 / journal / mixed-topic dump) into multiple MECE topic notes inside a sibling subfolder. Triggers on "拆分 / distill / organize / break down / 整理 messy notes / 流水 into structured topics", or when the user points at a single dense .md file and asks for MECE topic decomposition. Includes a post-delivery reflection loop that interviews the user and proposes updates to this very SKILL.md so the skill improves with every run.
---

# messy-to-mece — 把流水笔记拆成 MECE 主题文件

## 何时触发

- 用户指向一个杂乱的 markdown 文件（流水反思、项目笔记、interview dump、mixed thoughts），要求"拆分 / 整理 / distill / organize / break down / 重新整理"成若干主题文件
- 用户提到 "MECE"、"按主题分"、"分子文件"、"放到子文件夹"
- 文件特征：单文件 200+ 行、含多个主题、混杂事实 + 反思 + 工作流（流水形式）

## 核心承诺

1. **零信息损失** — 原始内容每一句都能在结构化版本中找到对应位置
2. **MECE** — 每段原文只落在一个主题文件中（mutually exclusive），且所有内容都被覆盖（collectively exhaustive）
3. **风险可见** — 不确定的片段用 `[?]` 标记，结尾汇总为开放问题列表
4. **可独立读取** — 任意一个主题文件单独打开能看懂，不必回查原文
5. **自改进** — 每次执行完成后通过反思 + interview 迭代这份 SKILL.md（见 §6）

## 工作流（6 个 Phase）

### Phase 1 — Discovery（理解）

不要立刻拆分。先做：

1. **完整读源文件**（一次性，不要 offset）
2. **读 sibling files**：同目录的 README.md、相邻 .md、上一级目录 README — 摸清文档生态、命名风格、是否有"项目层评估表"等已存在结构
3. **建立内容地图**（mental model）：原文行号 → 大致主题（不需要写下来，但要在 Phase 3 的 plan 里呈现）

⚠️ 此阶段如果用户授权 Plan agent / Explore agent，优先用 1 个 Explore — 不超过 1 个，避免过度调度。

### Phase 2 — Interview（4 问 + 1 备用）

用 **AskUserQuestion** 一次性发出 3-4 个核心问题（多选单选），不要分开问。**默认 4 个问题**：

| # | 问题 | 选项设计要点 |
|---|---|---|
| 1 | 笔记的用途？ | 个人知识库 / 面试 case 准备 / 公司可分享资产 / Both — 影响所有写作语气和保留度 |
| 2 | 跨主题的反思（方法论 / 行业元洞察）放哪？ | 留在子文件夹内 / 移到独立 methodology 文件夹 / Both + 交叉链接 |
| 3 | 专有名词（人名 / 内部缩写）怎么处理？ | 原样保留 / README 加 glossary / inline 标注角色 |
| 4 | 看不懂的碎片怎么办？ | 原样保留打 raw 标 / 尽力解读 + `[?]` / 现在就逐条问我 |

**只在用户答完后才进入 Phase 3**。如果回答里出现"Other"或意外路径，可追加 1-2 个 follow-up 问题。

### Phase 3 — Plan（写到 plan 文件）

进入 Plan Mode（如果还没在），把方案写到 plan 文件，至少包含：

1. **Context** — 为什么要做、源文件特征、用户的 4 个回答的总结
2. **输出结构** — `subfolder-name/{README + N 个主题文件}` 的目录树
3. **每个文件的内容设计** — 写什么、用哪些原文片段（行号引用）
4. **MECE 内容映射表** — 一张表：`原文行号 → 内容主旨 → 目标文件`，确保每段都有去处
5. **写作约定**（每文件遵守）：
   - 顶部 `> Last updated: YYYY/MM/DD`
   - 顶部 TL;DR（3-5 行概要）
   - `[?]` 标记 + 可选 *原文：xxx* 注释
   - 文末 "Related" 互链
   - 文末 "开放问题 / 待澄清" 收尾
6. **关键文件清单** — 新建 / 修改 / 不动
7. **验证方式** — MECE 自检 / 可读性自检 / `[?]` 数量审查

调用 ExitPlanMode 等用户批准。

### Phase 4 — Execute（写文件）

按 plan 一次写完所有文件：

- **TodoWrite** 每个文件作为一个 todo（一次性建好，依次 in_progress → completed）
- **保留原始文件** — 不要删源 `.md`，作为可回溯 raw source
- 顺序：README → 01 → 02 → ... → 最后一个
- 每个文件都遵守 §3.5 写作约定
- **不写 glossary**（除非 Phase 2 用户明确要 README glossary）

### Phase 5 — Verify（自检）

完成后立刻跑：

1. **关键术语 MECE 校验**：
   ```bash
   for term in <列出 30-60 个原文出现的关键名词 / 人名 / 缩写>; do
     hits=$(grep -l "$term" *.md 2>/dev/null | tr '\n' ' ')
     [ -z "$hits" ] && echo "MISSING: $term"
   done
   ```
   如果有 MISSING，检查是不是 spacing 变体（"8 大人群" vs "8大人群"），不是变体的话补内容
2. **`[?]` 标记列表**：`grep -n '\[?\]' *.md` — 输出给用户做 review
3. **行数 + 字节数报告**：让用户看到拆分后的总量级
4. 简短交付总结（用 markdown 表格列出新文件 + TL;DR + 各文件 [?] 数量）

### Phase 6 — Reflection（这是这个 skill 的特别之处）⭐

**在 Phase 5 交付后必须进入这一步，不要遗漏**。目的是：让 skill 越用越好。

#### 6.1 等用户先消化

不要在交付的同一条消息里追问。让用户先快速扫一眼成果（如果用户立刻说"完美"就直接进入 6.2，否则等用户回话）。

#### 6.2 用 AskUserQuestion 问 3-4 个 retrospective 问题

模板（每次执行可微调）：

| # | 问题 | 选项设计 |
|---|---|---|
| 1 | 主题切分本身怎么样？ | 完全合理 / 有 1-2 个应该合并 / 有 1-2 个应该拆开 / 整体重切 |
| 2 | Phase 2 的 4 个 interview 问题足够吗？ | 刚好 / 应该再多问 1-2 个（追问内容） / 多问了 / 应该改成开放式 |
| 3 | `[?]` 标记的方式有用吗？ | 有用、保留 / 太多干扰、应该收敛 / 不够、应该更激进标注 / 换成别的形式 |
| 4 | 写作约定（TL;DR / Last updated / Related / 开放问题）有缺失吗？ | 全部满意 / 应该加 X / 应该减 Y / 顺序应该调整 |

如果用户的回答触及"主题应该重切" — 主动 propose 重组方案，**不要直接改文件**，先达成共识。

#### 6.3 把反馈固化回 SKILL.md

用户答完后：

1. 把每条反馈翻译成对 SKILL.md 的具体修改（精确到段落）
2. 用 Edit 工具修改 SKILL.md（保留 frontmatter 不动）
3. 在 SKILL.md 末尾的 `## Changelog` 追加一行：
   ```
   - YYYY/MM/DD — <一句话本次学到的 / 调整的>（trigger: <项目名>）
   ```
4. 跑 `wc -l SKILL.md` 让用户看到 skill 的演进体积

#### 6.4 主动发现的改进

除了用户回答的 4 个问题之外，自己也主动观察：
- 这次执行哪些步骤反复来回（说明流程有 friction）
- 哪些 [?] 标记其实是因为我问得不够（应该把问题加进 Phase 2 模板）
- 哪些用户已经在 CLAUDE.md / 全局 memory 里说过的偏好我没有自动应用

把这些观察作为"Skill 自己也注意到的"插入 6.2 的回话中，让用户裁决是否纳入。

## 关键约定（每次执行一定遵守）

1. **不删源文件** — 保留为可回溯 raw source
2. **专有名词不解释**（除非用户在 Phase 2 选了"加 glossary"）
3. **`Last updated` 字段** — 每个新写 / 修改的 .md 顶部都要带（用户的 CLAUDE.md 全局规则）
4. **不创建多余文件** — 用户没要求就不写额外的 README、index、glossary
5. **MECE 内容映射表写入 plan 文件** — 这是给用户验证的最大杠杆
6. **每个主题文件结尾必带"Related"+"开放问题"两节** — 让文件互相挂钩、把不确定显式化

## 反模式（避免）

- ❌ 跳过 Phase 2 直接拆分（用户的 4 个偏好不一样，整个产物会跑偏）
- ❌ 把方法论 / 反思和项目事实混在同一个文件里（`reflections-methodology.md` 应该单独成文）
- ❌ 写 glossary 解释专有名词（用户已经知道）
- ❌ 大量 *斜体注释* 或 emoji 装饰（保持 markdown 干净）
- ❌ 跳过 Phase 6（这是 skill 区别于普通整理任务的关键点）
- ❌ 反思阶段直接改 SKILL.md 不让用户裁决

## 模版片段（可直接抄）

### TL;DR 段落
```markdown
# NN — 主题名

> Last updated: YYYY/MM/DD

## TL;DR

3-5 行概要。先讲核心结论 / 关键 framework / 反直觉发现。让未来速读时 30 秒能 grok 主旨。
```

### `[?]` 标记
```markdown
- 某个不确定的事实 [?]
- 某段难解读的句子 [?] *（原文："xxx xxx"）*
```

### 文末 Related 块
```markdown
---

## Related

- [01 — 商业模式](01-business-model.md) — 为什么相关：xxx
- [03 — 经销商对标](03-distributor-benchmarks.md) — 为什么相关：xxx
```

### 文末开放问题块
```markdown
## 开放问题 / 待澄清

- xxx 的具体含义 [?]
- 是否需要进一步调研 yyy？
```

## Changelog

- 2026/05/05 — Skill 初创，从 Apple-Project-25.md 拆分项目沉淀而来；包含 6 个 Phase + 反思自改进循环（trigger: 动势经历/Apple-Project）
- 2026/05/05 — 反思 #1：用户在 Apple-Project 执行结束后确认 — 主题切分（7 文件）/ Phase 2 四问 / `[?]` 标记 / 写作约定 全部满意，设计锁定，无结构性改动。
