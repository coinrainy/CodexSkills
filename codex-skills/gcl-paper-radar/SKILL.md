---
name: "gcl-paper-radar"
description: "周期性检索近三年图对比学习及可迁移到图对比学习的计算机视觉论文，结合本地状态执行去重、生成论文卡片与周报。适用于用户希望每周自动找新论文、避免重复阅读、沉淀结构化文献卡片，或为 GCL 方向持续寻找新 idea 的场景。"
---

# GCL 论文雷达

## 概览

把“每周找论文”变成稳定的文献管线。默认覆盖近三年的图对比学习论文，以及计算机视觉中可能迁移到图对比学习的 contrastive / self-supervised 方法论文。核心输出不是一串链接，而是：

- 去重后的论文清单
- 结构化论文卡片
- 每周 digest
- 可交给 Notion 的导入队列

## 工作流

1. 先读取本地状态。优先检查 `literature_pipeline/state/master_papers.csv`、`literature_pipeline/state/query_log.md`、`literature_pipeline/weekly_digests/` 和 `literature_pipeline/paper_cards/`，避免从空白状态重新开始。
2. 明确检索范围。默认时间窗是最近三年，默认优先级是：
- 直接相关：graph contrastive learning, graph self-supervised learning, graph representation learning
- 可迁移相关：contrastive / self-supervised learning in computer vision, multimodal pretraining, augmentation learning, negative mining, bootstrapping, curriculum
3. 进行在线检索时，区分“发现源”和“最终引用源”。
- 发现源可以更广：OpenReview、PMLR、CVF Open Access、arXiv、DBLP、Google Scholar、Semantic Scholar、OpenAlex、会议官网目录
- 最终写入卡片和周报时，优先使用一手来源。优先级依次为：论文主页、arXiv、OpenReview、CVF Open Access、PMLR、ACM Digital Library、IEEE Xplore、AAAI proceedings、IJCAI proceedings、期刊官网
- 代码仓库仅作补充，不把仓库 README 当成论文主结论来源
4. 按研究方向拆分来源主场。
- 图对比学习 / 图自监督主场：OpenReview（ICLR、NeurIPS、TheWebConf/WWW 等）、PMLR（ICML、CoRL 等）、ACM Digital Library（KDD、WWW）、AAAI proceedings、IJCAI proceedings、IEEE / Springer / Elsevier 期刊官网、arXiv
- 可迁移 CV 主场：CVF Open Access（CVPR、ICCV、ECCV）、OpenReview（若对应 venue 使用）、PMLR、arXiv、IEEE Xplore、期刊官网
5. 做两层筛选：
- 第一层筛掉明显无关、非近三年、非顶会顶刊的论文
- 第二层判断其对 GCL 的价值：直接可复现、机制可迁移、评测协议可迁移、仅作背景
6. 执行去重。按照以下键顺序建立 canonical id：
- DOI
- arXiv id
- OpenReview forum id / 会议官方 paper id
- 标准化标题（小写、去标点、去多余空格）
7. 对新论文生成卡片。默认写到 `literature_pipeline/paper_cards/`，每篇卡片至少包含：
- 基本信息
- 为什么和 GCL 相关
- 方法核心机制
- 可迁移点
- 你值得关注的风险或限制
- 建议的后续动作
如果目标是服务后续 `$gcl-idea-forge`，优先补齐 richer schema：
- 相关性判断
- 目标瓶颈
- 机制类别
- GCL 挂接点
- 不可直接迁移部分
- 最快验证线索
- Idea seed
8. 更新总表和周报。把新论文写回 `master_papers.csv`，并在 `literature_pipeline/weekly_digests/` 下维护周报。
9. 如果用户要同步到 Notion，衔接 `$paper-to-notion-curator`；如果 Notion 尚未配置，至少生成本地导入批次。

## 工作规则

- 处理“本周新论文”时，必须先做本地去重，再做 Notion 侧去重。
- 对时间敏感的信息必须在线核实，不要只凭旧记忆判断“最近三年”或“最新”。
- 如果发现源与一手来源不一致，卡片中的 `primary_url` 应优先落到一手来源，而不是搜索引擎聚合页。
- 推荐论文时，优先解释“为什么它值得你读”，而不是只罗列标题。
- 面向后续 idea 生成时，优先把“这篇论文具体补哪类 GCL 瓶颈”“哪一块最适合挂进现有代码”“哪一块不能直接搬”写清，而不是只写泛泛启发。
- 对 CV 论文要显式区分：
- 直接适用于图对比学习
- 需要中等改造才能迁移
- 仅能作为启发，不适合直接落地
- 如果同一论文出现 arXiv 版、会议版、期刊扩展版，优先保留信息最完整的一版，并在 `notes` 中记录版本关系。
- 默认使用中文输出分析、卡片和周报；论文名、会议信息、作者、链接保留英文。

## 资源

- 先用 `scripts/init_paper_radar_workspace.py` 初始化 `literature_pipeline/`。
- 需要 richer 论文卡片时，优先用 `scripts/init_rich_paper_card.py` 初始化卡片骨架。
- 当你需要更具体的检索词、会场范围、筛选与去重规则时，阅读 `references/search_playbook.md`。
- 如果用户要把结果落到 Notion，再衔接 `$paper-to-notion-curator`。

## 示例请求

- "Use $gcl-paper-radar，请帮我检索最近三年的图对比学习论文，并把本周新增项整理成 digest。"
- "Use $gcl-paper-radar，帮我找近三年 CV 中可能迁移到 graph contrastive learning 的论文，并和已有清单去重。"
- "Use $gcl-paper-radar，优先筛选 NeurIPS、ICLR、ICML、CVPR、ICCV、ECCV、KDD、WWW、TPAMI 里的相关论文。"
