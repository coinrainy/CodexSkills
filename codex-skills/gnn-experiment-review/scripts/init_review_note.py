from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# GNN 实验复盘：{experiment}

## 运行摘要

- 实验批次：{experiment}
- Baseline：{baseline}
- 数据集：{datasets}
- 主要指标：{metric}

## 改了什么

- 模型结构：
- 目标函数：
- 增强方式：
- 优化器或训练日程：
- 评测流程：

## 症状

- 平均值提升或下降：
- Seed 方差：
- 训练稳定性：
- 跨数据集一致性：

## 假设

| 排名 | 假设 | 类型 | 置信度 | 证据 | 快速验证 |
| --- | --- | --- | --- | --- | --- |
| 1 |  | code/science/unresolved |  |  |  |
| 2 |  | code/science/unresolved |  |  |  |
| 3 |  | code/science/unresolved |  |  |  |

## 下一批实验

1. 确认实验：
2. 去除式 ablation：
3. 敏感性检查：
4. 廉价诊断实验：

## 证伪条件

- 什么结果会削弱当前最强假设？
- 什么结果值得扩大实验规模？
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为 GNN 实验复盘创建 Markdown 笔记模板。")
    parser.add_argument("output", help="Path to the output Markdown file.")
    parser.add_argument("--experiment", default="Latest Runs")
    parser.add_argument("--baseline", default="TBD")
    parser.add_argument("--datasets", default="TBD")
    parser.add_argument("--metric", default="TBD")
    parser.add_argument("--force", action="store_true", help="Overwrite the output file if it exists.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    if output.exists() and not args.force:
        raise SystemExit(f"{output} already exists. Re-run with --force to overwrite.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        TEMPLATE.format(
            experiment=args.experiment,
            baseline=args.baseline,
            datasets=args.datasets,
            metric=args.metric,
        ),
        encoding="utf-8",
    )
    print(f"Wrote experiment review note to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
