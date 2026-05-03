from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# GNN Idea Backlog：{topic}

## 项目快照

- 主题：{topic}
- 当前 baseline：{baseline}
- 数据集：{datasets}
- 主要瓶颈：{problem}

## Idea 排序表

| Idea | 机制 | 预期收益 | 成本 | 风险 | 最快验证 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 重点 Idea 卡片

### Idea 1

- 主张：
- 为什么在这里可能有效：
- 最小代码改动：
- 最快实验：
- 主要混杂因素：
- 关键 ablation：

### Idea 2

- 主张：
- 为什么在这里可能有效：
- 最小代码改动：
- 最快实验：
- 主要混杂因素：
- 关键 ablation：

### Idea 3

- 主张：
- 为什么在这里可能有效：
- 最小代码改动：
- 最快实验：
- 主要混杂因素：
- 关键 ablation：

## 放弃标准

- 什么负结果会让我们放弃当前第一优先级的 idea？
- 什么结果值得进一步做更大规模 sweep？
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为 GNN 研究想法创建 Markdown backlog 模板。")
    parser.add_argument("output", help="Path to the output Markdown file.")
    parser.add_argument("--topic", default="GNN Project")
    parser.add_argument("--baseline", default="TBD")
    parser.add_argument("--datasets", default="TBD")
    parser.add_argument("--problem", default="TBD")
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
            topic=args.topic,
            baseline=args.baseline,
            datasets=args.datasets,
            problem=args.problem,
        ),
        encoding="utf-8",
    )
    print(f"Wrote idea backlog to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
