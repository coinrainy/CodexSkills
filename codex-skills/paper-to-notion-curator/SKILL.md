---
name: "paper-to-notion-curator"
description: "把本地结构化论文卡片同步到 Notion，执行数据库 schema 对齐、Notion 侧去重、批量导入和周报关联。适用于用户希望维护统一论文库、把每周新论文写入 Notion、并避免 Notion 内重复建卡的场景。"
---

# 论文入库到 Notion

## 概览

这个 skill 负责把本地论文卡片变成 Notion 里的可检索论文库。重点不是“机械拷贝内容”，而是保证：

- Notion 中不重复建卡
- 数据库字段一致
- 周报与论文页面有关系链接
- 本地状态能反写 notion page id

## 工作流

1. 先读取本地状态。优先看：
- `literature_pipeline/state/master_papers.csv`
- `literature_pipeline/state/notion_config.json`；若不存在，则参考 `notion_config.template.json`
- `literature_pipeline/notion_import/`
2. 确认 Notion 目标。如果用户没给数据库 id 或 page id：
- 先用 Notion 搜索现有 `Papers` / `Literature` / `Reading` 数据库或页面
- 如果没有合适库，先创建一个入口说明页或请用户指定目标库
3. 在创建新页面前，先做 Notion 侧去重。建议按以下顺序搜索：
- canonical id
- arXiv id / DOI
- 论文标题
4. 仅对 Notion 中不存在的论文创建新页面；对已存在页面，更新必要字段或把本周 digest 关系补上。
5. 创建或更新后，把 `notion_page_id` 写回本地总表，并把状态从 `new` / `triaged` 推进到 `imported`。
6. 如果有周报页，把本周新增论文关联到周报；如果没有周报页，至少生成一份本地 import batch。

## 工作规则

- 在 Notion 中写入前，必须先 fetch 目标 data source schema，再按真实字段名填属性。
- 不假设数据库属性名叫 `Title` 或 `Status`；必须以 fetch 结果为准。
- 如果用户还没有现成数据库，不要伪造一个 schema 并声称已经接通；应先用本地模板和说明页占位。
- Notion 侧的重复判断要比本地更严格，因为标题、缩写、版本号可能不同。
- 默认用中文写摘要、可迁移点和备注；保留论文标题、作者、venue、链接的英文原文。

## 资源

- 先用 `scripts/init_import_batch.py` 为待导入论文生成本地批次文件。
- 字段设计、推荐属性和本地到 Notion 的映射见 `references/notion_schema.md`。
- 如果论文尚未筛选完，先回到 `$gcl-paper-radar`，不要在 Notion 里直接做原始采集。

## 示例请求

- "Use $paper-to-notion-curator，请把本周新增论文同步到 Notion，并避免重复建卡。"
- "Use $paper-to-notion-curator，先检查 Notion 里有没有这些论文，再把缺失项导入。"
- "Use $paper-to-notion-curator，把本地 paper cards 导入 Papers 数据库，并关联到本周 digest。"
