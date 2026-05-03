# Idea 维度参考

## 适用场景

- 用户希望比快速头脑风暴更深入的想法生成
- 你需要更严格地给 idea 排序
- 项目已经有几轮失败尝试，需要更谨慎地筛选方向

## GNN 项目里高收益的想法维度

1. 视图设计
改变正样本对或扰动的形成方式。适合当前增强过于泛化或明显有信息损失的情形。

2. 传播控制
调整深度、残差流、归一化或自适应消息传播。适合已经出现过平滑或邻域噪声问题的情形。

3. 目标函数塑形
修改对比式、预测式、去偏式或校准式目标。适合表示质量和下游分数出现背离的情形。

4. 数据中心改进
清洗划分、重标注、重采样或分层。适合方差很大或数据集伪特征主导结果的情形。

5. 训练动态
curriculum、温度调度、多阶段训练或 hard negative 控制。适合优化明显不稳定的情形。

6. 鲁棒性与迁移
领域偏移测试、扰动鲁棒性、缺失特征鲁棒性或低标注迁移。适合项目需要比单纯 benchmark 提升更强的论文故事时。

## 排序打分标准

每个 idea 从 1 到 5 分打分：

- mechanism strength
- fit to current bottleneck
- implementation ease
- compute cost
- ablation clarity
- paper-story value

优先选择机制分高且首个实验验证速度快的方向。

## 建议输出格式

对每个入选 idea，至少给出：

- idea name
- why it should help this project
- minimal code change
- fastest convincing experiment
- likely failure mode
- ablation to validate the claim
