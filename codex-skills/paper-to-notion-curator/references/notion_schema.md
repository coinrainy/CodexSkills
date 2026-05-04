# 推荐 Notion Schema

如果你已经有现成论文库，优先复用原库；如果没有，建议直接使用中文属性名，减少后续阅读和维护成本。

## 1. 推荐属性

- `论文标题`：论文标题
- `规范ID`：本地 canonical id，用于稳定去重
- `论文链接`：论文主链接
- `代码链接`：代码仓库
- `年份`
- `会议或期刊`
- `类型`：GCL / CV-transfer / survey / benchmark
- `状态`：new / triaged / imported / reading / archived
- `相关性`：high / medium / low
- `周报归档`：关联到每周 digest 页
- `备注`：简短备注

## 2. 本地字段映射建议

`master_papers.csv` 中常用列与 Notion 属性的对应关系：

- `canonical_id` -> `规范ID`
- `title` -> `论文标题`
- `year` -> `年份`
- `venue` -> `会议或期刊`
- `track` -> `类型`
- `relevance` -> `相关性`
- `primary_url` -> `论文链接`
- `code_url` -> `代码链接`
- `status` -> `状态`
- `notes` -> `备注`

## 3. 去重策略

先查 `规范ID`，再查 `论文链接`，最后查 `论文标题`。标题搜索要容忍大小写和标点差异。

## 4. digest 关联建议

每周一个 digest 页面，至少包含：

- 本周新增直接相关论文
- 本周新增可迁移论文
- 本周最值得精读的 3 篇
- 潜在 idea
- 下一步阅读建议

把论文页关联到 `周报归档`，而不是只在 digest 中粘贴标题，方便后续回溯。
