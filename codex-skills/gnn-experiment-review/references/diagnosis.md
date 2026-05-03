# 实验诊断指南

## 适用场景

- 指标变化很小且噪声较大
- 多种症状同时出现
- 用户不只是要解释，还要下一批实验建议

## 从症状到假设的映射

1. 平均值提升但方差暴涨
- likely causes：收益很脆弱、seed 数不够、增强或采样导致不稳定
- next checks：补更多 seed、减弱增强强度、查看各 seed 的失败样本

2. Train 指标上升但 validation 不上升
- likely causes：过拟合、训练目标泄漏、预训练与评测不匹配
- next checks：更强正则、更早的模型选择、单独检查表示质量

3. 一个改动让所有数据集都退化
- likely causes：实现 bug、超参数尺度不兼容、预处理损坏
- next checks：只回退该改动的 ablation、单元级 sanity check、检查 tensor 统计量

4. 只在一个数据集上赢，其他都输
- likely causes：dataset-specific inductive bias、划分伪差异、增强不匹配
- next checks：按图统计特征分层、只调新组件、检查失败样例

5. Loss 不稳定或发散
- likely causes：学习率过高、温度或归一化设置有问题、稀疏算子数值不稳定
- next checks：减小 lr、检查 clamp 或 eps、定位 NaN 来源

## 下一批实验的设计原则

每一批实验都应回答一个尽量窄的问题。
坏的设计：五个互不相关的改动。
好的设计：一个确认实验、一个去除式 ablation、一个敏感性检查、一个诊断实验。

## 置信度标签

- high：有日志或重复现象直接支持
- medium：和症状一致，但还没有被隔离验证
- low：只是合理猜测，证据较弱
