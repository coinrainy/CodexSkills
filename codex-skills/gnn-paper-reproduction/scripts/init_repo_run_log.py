from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# 仓库运行日志：{repo_name}

## 目标

- 仓库：{repo_name}
- 论文：{paper}
- 主要任务：{task}
- 目标数据集：{dataset}
- 目标指标：{metric}

## 初始扫描

- 是否找到 README：
- 训练入口：
- 评测入口：
- 配置文件：
- 环境文件：
- 已有 checkpoint 或日志：
- 论文 PDF / 补充材料 / 个人笔记：
- 论文材料路径与关键信息摘录：

## 数据集准备

| 数据集 | 论文是否涉及 | 本地状态 | 下载来源/命令 | 保存路径 | 可读性验证 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 环境准备

| 步骤 | 命令或改动 | 原因 | 状态 |
| --- | --- | --- | --- |
| 1 |  |  |  |

## 关键实验记录

| 尝试 | 运行命令 | 目的 | 最终结果 | 产物/备注 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

## 报错与修复

| 报错 | 可能原因 | 修复方式 | 验证 |
| --- | --- | --- | --- |
|  |  |  |  |

## 关键代码改动

- 文件：
  改动：
  原因：

## 当前最好结果

- 运行命令：
- 最终结果：
- 数据集：
- Seed：
- Checkpoint：
- 备注：

## 复现差距

- 论文结果：
- 当前结果：
- 差距：
- 最可能原因：

## 下一步动作

1.
2.
3.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为以仓库为起点的 GNN 复现创建 Markdown 运行日志模板。")
    parser.add_argument("output", help="Path to the output Markdown file.")
    parser.add_argument("--repo-name", default="Unknown Repo")
    parser.add_argument("--paper", default="TBD")
    parser.add_argument("--task", default="Run the main experiment")
    parser.add_argument("--dataset", default="TBD")
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
            repo_name=args.repo_name,
            paper=args.paper,
            task=args.task,
            dataset=args.dataset,
            metric=args.metric,
        ),
        encoding="utf-8",
    )
    print(f"Wrote repo run log to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
