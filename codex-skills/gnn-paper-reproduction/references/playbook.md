# 复现操作手册

## 优先级

1. 先锁定论文中真正要对齐的表、图和实验结果。
2. 再锁定论文或代码中能找到的参数设置。
3. 最后再做大规模运行和结果解释。

如果前两步没有做完，不要直接进入“只顾着跑代码”的模式。

## 必须优先记录的信息

### 论文结果

- target claim：要复现的具体表格、图或结论段落
- dataset：数据集名称和划分协议
- metric：指标定义和汇报方式
- baseline list：表中一并出现的对照方法
- paper value：论文中报告的目标值、方差或误差条
- evidence：页码、表号、图号、截图位置或补充材料位置

### 参数设置

- model：编码器、层数、隐藏维度、投影头、归一化、dropout
- preprocessing：特征归一化、自环、邻接处理、采样前处理
- augmentation：edge drop、feature masking、subgraph sampling、view 生成方式
- optimization：优化器、学习率、权重衰减、scheduler、warmup、epoch、patience
- stochasticity：seed 数量、采样随机性、数据划分随机性
- evaluation：checkpoint 选择规则、linear probe/finetune、跨 seed 平均方式

## 参数来源的记录规则

- `paper`：论文或附录中直接给出
- `code`：代码、配置文件、默认参数或脚本中直接给出
- `inferred`：从上下文合理推断，但没有直接证据
- `unknown`：当前找不到可信证据

不要把 `code` 或 `inferred` 写成论文显式设置。

## PDF 证据提取 fallback

优先按下面顺序处理，不要第一步失败就停：

1. 用当前环境尝试运行 `scripts/extract_pdf_evidence.py`
2. 如果当前环境缺少 `pypdf`，改用 bundled runtime 的 Python 运行同一脚本
3. 如果能提取，记录页码、表号、命中的原文片段和结构化结果
4. 如果仍然失败，在背景文档里记录：
   - 尝试过的命令
   - 使用的环境
   - 具体报错
   - 当前降级状态，例如 `pending paper evidence`
5. 降级后继续推进代码复现，但不要把论文结果栏留成无来源的空白断言

## 结果差距分析模板

- observed delta：
- most likely cause：
- strongest evidence：
- counter-evidence：
- cheapest next check：
- what result would change the diagnosis：

## 常见隐藏变量

1. 数据划分协议不同。
2. 评测协议不同。
3. 图增强强度不同。
4. 框架默认值不同。
5. 有效训练预算不同。

如果结果差距很大，先回头检查这五类，而不是第一时间重写模型。
## Evidence retention rule

- If a paper PDF exists but extraction still fails, retain the paper-results rows with an evidence-status field instead of deleting or omitting them.
- Preferred fallback fields:
  - `paper_value`: `pending paper evidence`
  - `evidence_status`: `extract_failed`
  - `pdf_path`: local PDF path
  - `attempted_backends`: parser/backend list
  - `attempted_commands`: exact commands
  - `error_summary`: concrete error text
