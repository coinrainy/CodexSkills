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

## 仓库扫描

- README：
- 主入口：
- 配置文件：
- 依赖文件：
- 数据集要求：
- 已有输出：

## 环境准备

| 步骤 | 命令或改动 | 原因 | 状态 |
| --- | --- | --- | --- |
| 1 |  |  |  |

## 命令历史

| 尝试 | 命令 | 目的 | 结果 | 备注 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

## 报错与修复

| 报错 | 根因猜测 | 修复方式 | 验证 |
| --- | --- | --- | --- |
|  |  |  |  |

## 已确认可用的入口

- Train：
- Eval：
- Config：

## 当前状态

- 执行状态：
- 当前完成到哪一步：
- 主要 blocker：

## 下一步动作

1.
2.
3.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为 GNN 仓库执行创建 Markdown 运行日志模板。")
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
