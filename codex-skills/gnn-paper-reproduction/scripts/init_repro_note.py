from __future__ import annotations

import argparse
from pathlib import Path


RESULTS_TEMPLATE = """# 复现实验结果：{paper}

## 目标

- 论文：{paper}
- 目标结果或表格：{claim}
- 数据集：{dataset}
- 主干模型：{backbone}
- 指标：{metric}
- 源仓库：{repo}

## 论文实验结果记录

| 数据集 | 表/图 | 方法 | 指标 | 论文结果 | 误差条/方差 | 来源页码/位置 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## 论文证据提取状态

- 状态：`pending`
- PDF 路径：
- 已尝试方法：
- 当前结论：

## 当前复现实验结果

| 数据集 | 运行配置 | 当前结果 | 运行时间 | 产物 | 备注 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 论文结果 vs 当前结果

| 数据集 | 指标 | 论文结果 | 当前结果 | 差距 | 初步解释 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 关键实验记录

| 尝试 | 运行命令 | 目的 | 最终结果 | 产物/备注 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

## Sanity Check

- 极小子集过拟合：
- 验证数据划分完整性：
- 验证随机种子控制：
- 验证增强统计量：
- 验证评测流程：

## 结果差距

- 论文报告指标：
- 当前指标：
- 差距：
- 最可能解释：

## 下一步实验

1.
2.
3.
"""


CONTEXT_TEMPLATE = """# 复现背景与过程：{paper}

## 目标

- 论文：{paper}
- 目标结果或表格：{claim}
- 数据集：{dataset}
- 主干模型：{backbone}
- 指标：{metric}
- 源仓库：{repo}

## 关联文档

- 实验结果文档：`{results_filename}`

## 材料清单

- 本地代码：
- 配置文件：
- Checkpoint：
- 日志：
- 论文 PDF / 补充材料 / 个人笔记：
- 论文材料路径与关键信息摘录：

## PDF 证据提取记录

| 尝试 | 运行命令/方法 | 环境 | 最终结果 | 备注 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

## 参数设置记录

| 类别 | 参数 | 当前记录值 | 来源 | 状态 | 证据 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| model |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |
| preprocessing |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |
| augmentation |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |
| optimization |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |
| schedule |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |
| evaluation |  |  | paper/code/inferred/unknown | explicit/inferred/unknown |  |  |

## 数据集准备

| 数据集 | 论文是否涉及 | 本地状态 | 下载来源/命令 | 保存路径 | 可读性验证 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 忠实度台账

| 项目 | 取值 | 状态 | 敏感性 | 证据 |
| --- | --- | --- | --- | --- |
| split |  | explicit/inferred/unknown |  |  |
| preprocessing |  | explicit/inferred/unknown |  |  |
| augmentation |  | explicit/inferred/unknown |  |  |
| optimizer |  | explicit/inferred/unknown |  |  |
| evaluation |  | explicit/inferred/unknown |  |  |

## 最小复现阶梯

1. 先补齐实验结果文档中的论文结果记录表。
2. 再补齐本文件中的参数设置记录表。
3. 确认数据集与划分协议。
4. 不加额外改动先复现 baseline。
5. 在单个 seed 上复现主方法。
6. 用论文的 seed 数量或最接近的可行代理重跑。

## 环境与依赖判断

- Python：
- Torch：
- Torch Geometric：
- CUDA：
- 其他依赖：
- 结论：

## 代码与兼容性修改记录

| 尝试 | 修改文件/命令 | 目的 | 最终结果 | 备注 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |

## 高风险缺失信息

- 
- 
- 
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为 GNN 论文复现创建双文档 Markdown 模板。")
    parser.add_argument("output", help="Path to the output Markdown file.")
    parser.add_argument("--paper", default="Unknown Paper")
    parser.add_argument("--claim", default="Main result")
    parser.add_argument("--dataset", default="TBD")
    parser.add_argument("--backbone", default="TBD")
    parser.add_argument("--metric", default="TBD")
    parser.add_argument("--repo", default="TBD")
    parser.add_argument("--force", action="store_true", help="Overwrite the output file if it exists.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    stem = output.stem
    if stem.endswith("_results") or stem.endswith("_context"):
        stem = stem.rsplit("_", 1)[0]

    results_output = output.with_name(f"{stem}_results.md")
    context_output = output.with_name(f"{stem}_context.md")

    for path in (results_output, context_output):
        if path.exists() and not args.force:
            raise SystemExit(f"{path} already exists. Re-run with --force to overwrite.")

    format_kwargs = {
        "paper": args.paper,
        "claim": args.claim,
        "dataset": args.dataset,
        "backbone": args.backbone,
        "metric": args.metric,
        "repo": args.repo,
        "results_filename": results_output.name,
    }

    results_output.write_text(RESULTS_TEMPLATE.format(**format_kwargs), encoding="utf-8")
    context_output.write_text(CONTEXT_TEMPLATE.format(**format_kwargs), encoding="utf-8")
    print(f"Wrote reproduction result note to {results_output}")
    print(f"Wrote reproduction context note to {context_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
