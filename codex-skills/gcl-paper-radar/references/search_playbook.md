# 检索与去重手册

## 1. 默认覆盖范围

- 图学习：graph contrastive learning, graph self-supervised learning, graph representation learning, graph pretraining
- 视觉迁移：contrastive learning, self-distillation, bootstrap, masked modeling, augmentation learning, hard negative mining, curriculum
- 时间范围：默认最近三年；若用户指定“本周新增”，优先看最近 7 到 14 天的新条目

## 2. 推荐 venue 清单

- 图学习 / 通用机器学习：NeurIPS, ICLR, ICML, KDD, WWW, AAAI, IJCAI, TKDE, TPAMI, JMLR
- 视觉：CVPR, ICCV, ECCV, TPAMI

## 3. 推荐来源分层

### A. 图对比学习主场来源

- OpenReview：ICLR、NeurIPS、TheWebConf/WWW 等带公开页面的论文
- PMLR：ICML 等机器学习会议正式 proceedings
- ACM Digital Library：KDD、WWW 等 ACM venue
- AAAI / IJCAI 官方 proceedings
- 期刊官网：TPAMI、TKDE、JMLR 等
- arXiv：补充最新版本、校对标题与版本关系

### B. 可迁移 CV 主场来源

- CVF Open Access：CVPR、ICCV、ECCV
- OpenReview：若对应 venue 使用
- PMLR：少量视觉相关 ML 论文
- IEEE Xplore / 期刊官网：TPAMI 等
- arXiv：补充最新版本与作者提供的扩展稿

### C. 发现源

这些来源适合“发现候选论文”，但不应优先作为最终卡片里的主链接：

- DBLP
- Google Scholar
- Semantic Scholar
- OpenAlex
- 会议官网目录页

## 4. 推荐检索词

- "graph contrastive learning site:openreview.net"
- "graph self-supervised learning site:openreview.net"
- "graph pretraining contrastive learning arXiv"
- "CVPR contrastive learning augmentation learning"
- "ICCV self-supervised representation learning negative mining"
- "ECCV bootstrap self-distillation representation learning"
- "KDD graph self-supervised learning site:dl.acm.org"
- "WWW graph contrastive learning site:openreview.net"
- "TPAMI graph self-supervised learning"
- "CVPR patch-level contrastive learning site:openaccess.thecvf.com"
- "ICCV conditional contrastive learning site:openaccess.thecvf.com"

## 5. 初筛问题

- 这篇论文是否在最近三年内公开？
- venue 是否达到用户要求的顶会顶刊范围？
- 论文的核心机制是否可能迁移到 GCL，而不是只适用于图像像素空间？
- 论文是否已经在 `master_papers.csv` 或 Notion 中出现？

## 6. 来源选择规则

1. 用发现源找到候选后，尽量回到正式论文页。
2. 如果同时存在 OpenReview、PMLR、CVF、arXiv：
- 已正式发表时，优先正式 proceedings 页面
- 若正式页面信息不全，可在 `notes` 中补 arXiv 版本关系
3. 对 KDD / WWW / AAAI / IJCAI / TPAMI 论文，优先官网或官方出版平台，不优先第三方转录页。

## 7. 去重键优先级

1. DOI
2. arXiv id
3. OpenReview forum id 或官方 paper id
4. 标准化标题

标题标准化建议：

- 全部转小写
- 去掉标点
- 连续空白折叠为单空格
- 去掉前后空格

## 8. 论文卡片最小字段

- 标题
- 年份
- venue
- 直接来源链接
- 代码链接
- 与 GCL 的关系
- 核心机制
- 可以迁移的模块
- 主要风险
- 建议下一步

## 9. 面向 idea 生成的 richer 字段

如果这批论文后续要喂给 `$gcl-idea-forge`，建议每张卡至少再补：

- `相关性判断`：`direct / transferable_high / transferable_medium / inspiration_only`
- `目标瓶颈`：这篇论文真正想修什么问题
- `机制类别`：`view / sampling / objective / architecture / curriculum / efficiency`
- `GCL 挂接点`：最小代码或方法入口应该落在哪
- `不可直接迁移部分`：哪些假设只在原论文域成立
- `最快验证线索`：1 到 3 天内最容易验证的切入口
- `Idea seed`：一句话说明它最值得衍生的研究方向

这些字段的目的不是提前替 `$gcl-idea-forge` 写完整 idea，而是让它少做猜测，多做组合。

## 10. digest 建议结构

- 本周新增直接相关论文
- 本周新增可迁移论文
- 最值得精读的 3 篇
- 候选 idea 列表
- 与已有 backlog 的关系
