# Idea Synthesis Playbook

## 适用场景

- 你已经有一批新论文，但还没有把它们压缩成可执行研究方向
- 用户要的不只是“值得读什么”，而是“下一步具体做什么”
- 你需要把单篇论文启发，转成跨论文组合的可验证 idea

## 推荐流程

1. 先做单篇抽取
- paper
- bottleneck targeted
- mechanism
- transplantable unit
- likely integration point

2. 再做组合，不要直接跳到结论
- 单篇迁移：把一篇论文的核心机制直接变成 GCL 插件
- 同类叠加：把两篇都在解决同一瓶颈的方法合并
- 异类拼接：把 view / sampling / loss / curriculum 分别来自不同论文
- 反向约束：先从失败风险出发，寻找能降低该风险的机制

3. 排序时建议使用 1 到 5 分
- mechanism strength
- fit to current GCL bottleneck
- implementation ease
- compute affordability
- ablation clarity
- paper-story value

## 命名规则

- sprint 文件名：`YYYY-Www-gcl-idea-sprint-NN.md`
- sprint_id：与文件 stem 完全一致，例如 `2026-W19-gcl-idea-sprint-02`
- backlog id：`gcl-{sprint_id}-idea-01`
- 如果用户指定别的前缀，可替换最前面的 `gcl`，但不要改动后半段结构

这样做的目的是让：
- 同一周的多期 brainstorming 文件可以稳定排序
- backlog id 能直接反推来源 sprint
- 后续同步到 Notion 或总表时更容易建立引用关系

## 默认增量逻辑

- 默认读取最新一周的 digest
- 默认只纳入 `master_papers.csv` 里属于该周、且尚未出现在旧 sprint 文件中的论文卡
- 如果本周论文已经全部进入旧 sprint，默认不再重复创建新文件，而是提示用户显式覆盖
- 若要强行重做旧论文，可以用显式 `paper-card` 或启用 `include-covered`

## 高价值组合模式

### 1. 视图构造 + 训练调度

当一篇论文提出更好的 graph view，另一篇论文提出 progressively harder augmentation 或 curriculum 时，可以优先考虑组合。

### 2. 正样本构造 + 校准目标

如果一篇论文在优化 positives，另一篇论文在减少 similarity bias 或 consistency bias，它们通常适合拼接成“采样 + loss”组合。

### 3. 原型或软匹配 + 多粒度目标

prototype、cluster-aware grouping、optimal transport、soft matching 与 node-subgraph-graph 多层目标经常能形成较强叙事，但要特别检查复杂度。

### 4. 结构压缩或轻量化 + 单视图 GCL

这类方向通常实现成本较低，适合作为 low-risk 或 mid-risk 的快速试验入口。

## 落地检查项

每个入选 idea 都至少检查：
- 是否能说清楚它试图修复的 GCL 失败模式
- 是否能挂接到现有 baseline，而不是重写整个 pipeline
- 是否能设计一个 1 到 3 天内完成的 smoke experiment
- 是否有至少一个必要 ablation
- 是否有明确 stop condition

## 深度认知验收

不要只验证“有没有 idea”，还要验证“是不是真的理解了论文”。每个入选 idea 至少补齐：

- source papers
- source cards
- paper-by-paper bottleneck
- paper-by-paper mechanism
- transferable unit
- non-transferable part or caveat
- why the papers can be combined
- biggest uncertainty

如果缺任意一项，说明当前更像摘要整理，还不到可执行 idea。

## Feasibility Gate

每个 shortlist idea 默认检查以下 5 项：

- at least one direct GCL paper
- clear code hook
- 1 to 3 day smoke experiment
- at least one required ablation
- not dependent on large-scale sweep

建议标记为：
- `pass`: 五项都满足，或只剩很小的不确定点
- `revise`: 机制有价值，但还缺关键实现或验证信息
- `reject`: 当前更像空想、综述式总结或高成本模糊方向

## 建议输出格式

每个重点 idea 建议至少包含：
- backlog id
- idea name
- one-sentence claim
- source papers
- source cards
- why the papers can be combined
- paper-level evidence chain
- why it may help GCL
- minimal implementation path
- fastest experiment
- ablation plan
- failure mode
- stop condition
- biggest uncertainty
- feasibility gate status
