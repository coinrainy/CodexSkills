---
name: "gcl-idea-forge"
description: "围绕一批新发现的图对比学习或可迁移 CV 论文，提炼机制信号、交叉组合并排序可执行 idea，最终产出清晰的本地 Markdown idea sprint 文件。适用于用户已经用论文雷达找到新论文，想进一步做头脑风暴、沉淀具体研究方向、并给出最小实验路径的场景。"
---

# GCL Idea Forge

## 概览

这个 skill 负责把“新找到一批论文”推进成“有操作方向、且经过可行性验收的下一批 idea”。

默认输入不是一篇论文，而是一个论文批次，通常来自：
- `literature_pipeline/weekly_digests/`
- `literature_pipeline/paper_cards/`
- `literature_pipeline/state/master_papers.csv`

默认输出不是聊天里的口头 brainstorming，而是落地到本地的 idea sprint 文档。默认写到：
- `literature_pipeline/idea_sprints/`

默认初始化行为是：
- 自动读取最新的 `weekly_digests/*.md`
- 自动从 `state/master_papers.csv` 找到该周论文卡
- 自动跳过已经出现在旧 `idea_sprints/` 文件里的论文卡
- 自动生成下一期 sprint 文件名

## 工作流

1. 先读取本地状态。优先查看本周或用户指定周次的：
- `weekly_digests/*.md`
- `paper_cards/*.md`
- `state/master_papers.csv`

2. 识别本批论文的机制主题，而不是只抄摘要。优先抽取：
- 这篇论文想解决什么瓶颈
- 它引入了什么机制
- 哪一部分最可能迁移到 GCL
- 它更适合作为 baseline、插件、训练策略、还是评测协议启发
如果上游卡片已经有 richer 字段，优先直接消费：
- `相关性判断`
- `目标瓶颈`
- `机制类别`
- `GCL 挂接点`
- `不可直接迁移部分`
- `最快验证线索`
- `Idea seed`

3. 把单篇论文信号整理成“可组合部件”。至少区分：
- view / augmentation design
- positive or negative sampling
- objective or calibration
- architecture or propagation
- prototype / clustering / matching
- curriculum / schedule
- efficiency or compression

4. 只保留可执行 idea。每个入选 idea 至少要回答：
- 一句话主张是什么
- 它来自哪些论文信号
- 对应的 paper card 是什么
- 每篇来源论文分别解决什么 bottleneck
- 每篇来源论文真正提供了什么 mechanism
- 哪些部分可以迁移，哪些部分不能直接迁移
- 为什么这些论文信号能组合，而不是硬拼
- 最小代码改动入口在哪里
- 最快验证实验是什么
- 关键 ablation 是什么
- 什么结果会让我们停止继续投入
- 当前最不确定的地方是什么

5. 默认输出 3 到 5 个排序后的 idea，而不是堆很多空泛方向。排序时同时考虑：
- 预期收益
- 实现成本
- 与当前 GCL 工作流的贴合度
- 是否容易被证伪
- 是否能形成清晰论文叙事

6. 必须把结果落成本地文件。先用 `scripts/init_idea_sprint.py` 初始化模板，再填充完整内容。默认情况下：
- 不传参数时，脚本会自动为“最新周次中尚未进入 idea sprint 的论文”创建新文件
- sprint 文件名统一为 `literature_pipeline/idea_sprints/YYYY-Www-gcl-idea-sprint-NN.md`
- sprint 内部的 `sprint_id` 与文件 stem 保持一致
- backlog id 统一为 `{prefix}-{sprint_id}-idea-01` 这种格式，默认 `prefix=gcl`

7. 若用户后续要同步到 Notion，先保留本地文件为主，再按需衔接 `$paper-to-notion-curator`；不要把 Notion 页面当作唯一工作底稿。

## 工作规则

- 默认优先基于“本周新增”或“当前批次新增”论文做 brainstorming，不要混入太多旧论文，除非它们是必要对照。
- 默认只纳入“本周新增且尚未进入旧 sprint”的论文；如需重做旧论文，可显式指定 `--paper-card` 或 `--include-covered`。
- 直接相关的 GCL 论文优先于可迁移 CV 论文；但高质量的跨论文组合可以混搭两类来源。
- 不要把“论文摘要换句话说”当成 idea，必须明确迁移到当前 GCL 语境后的改动入口。
- 每个保留在 shortlist 的 idea 都必须通过最小 feasibility gate：
- 至少 1 篇 direct GCL 论文
- 明确的代码挂接点
- 1 到 3 天内可完成的 smoke experiment
- 至少 1 个必要 ablation
- 不依赖大规模 sweep 才能成立
- 每个 idea 必须标注风险等级：`low-risk`、`mid-risk` 或 `high-risk`。
- 每个 idea 必须给出 1 个最快验证实验，优先选择 1 到 3 天可完成的路径。
- 每个 idea 必须给出 stop condition，避免无限制扩展无效方向。
- 如果做不到论文证据链、机制迁移链和 feasibility gate，就把该方向放进 `Rejected Or Deferred Ideas`，不要硬保留。
- 同一周内如果需要多个 sprint，按 `-01`、`-02`、`-03` 递增，不要混用无序命名。
- 默认使用中文输出分析和 Markdown；论文名、作者、venue、路径、命令、链接保留英文。

## 交付物

完成一次任务时，至少产出一个本地 Markdown 文件，包含：
- 本批论文概览
- 论文理解与证据链
- 机制信号归纳表
- 排序后的 idea shortlist
- 每个重点 idea 的执行卡片
- 每个 idea 的 feasibility gate
- rejected / deferred 方向
- 推荐优先顺序
- stop conditions 与下一步实验建议

## 资源

- 先用 `scripts/init_idea_sprint.py` 初始化本地 idea sprint 模板。
- 当你需要更细的组合方式、打分标准和落地检查项时，阅读 `references/idea_synthesis_playbook.md`。
- 如果论文批次本身还没整理好，先回到 `$gcl-paper-radar`；如果要同步结果到 Notion，再衔接 `$paper-to-notion-curator`。

## 示例请求

- "Use $gcl-idea-forge，请直接读取本周尚未进入 idea sprint 的新论文，输出 3 到 5 个可执行的 GCL idea，并写入下一期本地 sprint 文件。"
- "Use $gcl-idea-forge，请直接读取本周尚未进入 idea sprint 的新论文，并且只保留能说清论文证据链、机制迁移链和 feasibility gate 的 idea。"
- "Use $gcl-idea-forge，请基于 `literature_pipeline/weekly_digests/2026-W19.md` 和本周 paper cards，输出 3 到 5 个可执行的 GCL idea，并写入本地 idea sprint 文件。"
- "Use $gcl-idea-forge，请围绕本周新增论文做跨论文组合，优先找 low-risk 和 mid-risk 的 idea，给出最小实验方案。"
- "Use $gcl-idea-forge，请从 direct GCL 论文和 transferable CV 论文各抽取机制，帮我形成一份可排序的研究 backlog。"
