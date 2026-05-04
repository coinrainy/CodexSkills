---
name: "gnn-paper-reproduction"
description: "端到端复现 GNN 论文或原始代码仓库：先提取并记录论文中的目标实验结果，再检查论文或代码里的参数设置并写入复现文档，随后识别训练与评测入口、跑通代码、修复环境或兼容性问题、补全缺失超参数，并分析结果差距。适用于用户要求复现论文、跑通 GNN/GCL 仓库、对齐论文主表、补全实验设置、排查复现失败，或希望持续保留结构化实验记录的场景。"
---

# GNN 论文复现

## 概览

把论文、代码仓库和实验目录整理成一个可执行、可追溯、可对照论文主结果的复现流程。默认先做“证据记录”，再做“运行验证”：

1. 先记录论文里真正要对齐的实验结果。
2. 再记录论文或代码里能找到的参数设置。
3. 然后跑通最小实验、修复阻塞、逐步逼近论文结果。

如果论文 PDF、补充材料、README、配置文件、脚本、checkpoint 或日志同时存在，优先建立它们之间的证据链，而不是只盯着一个入口文件。

## 工作流

1. 明确复现目标。优先锁定论文中要对齐的表、图或主结论，记录：
   - 论文名
   - 目标表格或图编号
   - 数据集
   - 指标
   - 主模型
   - 允许误差或预期差距
2. 在做任何训练前先建立复现笔记。优先用 `scripts/init_repro_note.py` 创建双文档模板，并持续更新，不要等最后回填：
   - `*_results.md`：主要记录论文结果、当前实验结果、逐项对照和关键实验输出
   - `*_context.md`：主要记录材料、参数、环境、数据集准备、忠实度台账和修复过程
3. 先看论文实验结果并记录。只要本地存在论文 PDF、截图、补充材料或作者说明，就优先抽取并写入文档：
   - 目标实验的论文数值
   - 对应数据集和指标
   - 对照方法名
   - 结果来自哪一页、哪张表、哪张图
   - 默认优先使用 Codex bundled runtime 的 Python 运行 `scripts/extract_pdf_evidence.py`
   - 只有当前环境已经明确可用且这样做更方便时，才退回普通 Python
   - 如果仍然无法提取，明确记录“已尝试的方法 + 失败原因 + 下一步备用方案”，不要只写“缺少工具”
4. 再检查参数设置并记录。优先从论文正文、附录、配置文件、训练脚本、命令行参数和默认值中收集：
   - 模型结构参数
   - 预处理和增强参数
   - 优化器、学习率、权重衰减、调度器
   - epoch、batch size、patience、early stopping
   - seed 数量、划分协议、评测协议
   - 每项参数的来源：`paper`、`code`、`inferred` 或 `unknown`
5. 审查本地材料。检查仓库结构、配置文件、README、脚本、checkpoint、日志，以及代码目录附近的论文 PDF、补充材料、截图和笔记。
6. 处理数据集准备。若论文涉及多个数据集，默认把这些数据集都纳入准备清单，并记录本地状态、来源、保存路径和可读性验证。
7. 建立忠实度台账。把关键设置按 `explicit`、`inferred`、`unknown` 分类，尤其标记高敏感项，例如数据划分、增强方式、评测协议和 seed 聚合方式。
8. 先跑最小但忠实的实验切片。优先选择一个目标数据集、一个 seed 和论文主模型，先验证训练链路、损失、评测和设备路径。
9. 把环境与兼容性修复当作一线任务。每次修复都写进文档，说明原报错、原因、修改点和影响范围。优先最小改动，不悄悄改变原方法。
10. 在追最终指标前先做 sanity check。至少检查：
   - 极小子集是否能过拟合
   - 划分是否符合论文协议
   - 单 batch 的张量形状和统计量是否合理
   - 随机种子是否真实生效
   - 关闭关键模块后效果是否按预期下降
11. 对照论文结果分析差距。把当前结果与“论文结果记录表”逐项比较，再判断差距更像实现问题、环境问题、超参数缺失，还是论文描述不充分。

## 记录要求

- 论文实验结果记录必须先于大规模训练记录，并优先写进 `*_results.md`。
- 参数设置记录必须包含“值 + 来源 + 状态 + 备注”，不要只写一个默认值。
- 非结果类信息优先写进 `*_context.md`，避免把环境、修复过程和结果表混在一起。
- PDF 证据提取失败时，要把尝试顺序、执行命令、报错原因和当前降级状态写进 `*_context.md`。
- 如果论文和代码冲突，把两者都记下来，并注明当前运行采用哪一个。
- 如果只能从代码推断参数，必须标注为 `inferred`，不要伪装成论文显式设置。
- 如果拿不到论文 PDF 或不能稳定提取文本，要把这个阻塞单独写进文档，并在 `*_results.md` 里把对应结果标成 `pending paper evidence`。
- Markdown 记录实验时，优先使用“运行命令 + 目的 + 最终结果 + 产物/备注”的表格格式。

## 工作规则

- 优先最小、可证伪、忠实于原方法的复现路径，而不是为了跑通大改代码。
- 在调参前先对齐论文的评测协议、seed 协议和结果汇报方式。
- 明确区分“论文中的数值”“代码默认值”“当前实际运行值”。
- 结论要说明它来自真实执行、文档证据还是合理推断。
- 默认使用中文回复用户，默认使用中文撰写实验记录、分析结论和 Markdown 文档；代码、命令、路径、报错原文和术语保留英文。

## 交付内容

完成一次复现任务时，至少输出：

- 简短状态总结
- 两个复现笔记路径
- 论文实验结果记录表
- 参数设置记录表
- 忠实度台账
- 关键运行命令与关键代码改动
- 当前结果与论文结果的逐项对照
- 风险最高的缺失信息
- 最值得做的 1 到 3 个后续实验
- 当前差距更像科学问题还是实现问题的判断

## 资源

- 用 `scripts/init_repro_note.py` 在正式工作前创建复现笔记模板。
- 用 `scripts/extract_pdf_evidence.py` 提取论文 PDF 文本与页码证据时，默认优先使用 Codex bundled runtime 的 Python 运行该脚本；只有当前环境已明确可用时才退回普通 Python。
- 当用户要求完整记录“扫描-运行-报错-修复-结果”闭环时，使用 `scripts/init_repo_run_log.py`。
- 当论文缺失细节、代码与论文冲突、或结果差距难解释时，阅读 `references/playbook.md`。

## 示例请求

- "Use $gnn-paper-reproduction，先整理这篇 GCL 论文主表结果，再复现 Cora 上的主结果。"
- "Use $gnn-paper-reproduction，检查这个仓库，记录论文和代码里的参数设置，并判断缺了哪些超参数。"
- "Use $gnn-paper-reproduction，跑通这个原始仓库，修复训练阻塞问题，同时保留完整复现记录。"
## PDF Evidence Guardrail

- If a local paper PDF exists, do not drop the paper-results section just because extraction failed.
- Always keep a dedicated paper-evidence block in `*_results.md` or `*_context.md`.
- At minimum, record:
  - PDF path
  - target table / figure / dataset / metric still missing
  - extraction commands attempted
  - parser/backend attempted
  - concrete error text
  - current downgrade status such as `pending paper evidence`
- Treat `pending paper evidence` as a temporary evidence-status marker, not as a substitute for a paper result and not as permission to omit the row.
- When `scripts/extract_pdf_evidence.py` returns a structured error payload, copy the key fields into the reproduction notes instead of collapsing them into a generic "tool missing" sentence.
