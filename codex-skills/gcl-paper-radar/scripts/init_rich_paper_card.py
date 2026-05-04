from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# {short_title}

- 标题：`{title}`
- 年份 / venue：{year} / {venue}
- 一手来源：{primary_source}
- 代码链接：{code_url}
- 与 GCL 的关系：{relation}
- 相关性判断：{relevance_judgment}
- 目标瓶颈：{bottleneck}
- 机制类别：{mechanism_family}
- 核心机制：{mechanism}
- GCL 挂接点：{gcl_hook}
- 可迁移点：{transferable_unit}
- 不可直接迁移部分：{non_transferable_part}
- 最快验证线索：{fast_validation_cue}
- Idea seed：{idea_seed}
- 风险或限制：{risks}
- 建议后续动作：{next_step}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a richer paper card template for gcl-paper-radar."
    )
    parser.add_argument("output", help="Path to the output Markdown file.")
    parser.add_argument("--short-title", default="Paper")
    parser.add_argument("--title", default="TBD")
    parser.add_argument("--year", default="TBD")
    parser.add_argument("--venue", default="TBD")
    parser.add_argument("--primary-source", default="[TBD](https://example.com)")
    parser.add_argument("--code-url", default="N/A")
    parser.add_argument("--relation", default="直接相关 / 可迁移 / 仅启发")
    parser.add_argument(
        "--relevance-judgment",
        default="direct / transferable_high / transferable_medium / inspiration_only",
    )
    parser.add_argument("--bottleneck", default="TBD")
    parser.add_argument(
        "--mechanism-family",
        default="view / sampling / objective / architecture / curriculum / efficiency",
    )
    parser.add_argument("--mechanism", default="TBD")
    parser.add_argument("--gcl-hook", default="TBD")
    parser.add_argument("--transferable-unit", default="TBD")
    parser.add_argument("--non-transferable-part", default="TBD")
    parser.add_argument("--fast-validation-cue", default="TBD")
    parser.add_argument("--idea-seed", default="TBD")
    parser.add_argument("--risks", default="TBD")
    parser.add_argument("--next-step", default="TBD")
    parser.add_argument("--force", action="store_true", help="Overwrite if the file exists.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    if output.exists() and not args.force:
        raise SystemExit(f"{output} already exists. Re-run with --force to overwrite.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        TEMPLATE.format(
            short_title=args.short_title,
            title=args.title,
            year=args.year,
            venue=args.venue,
            primary_source=args.primary_source,
            code_url=args.code_url,
            relation=args.relation,
            relevance_judgment=args.relevance_judgment,
            bottleneck=args.bottleneck,
            mechanism_family=args.mechanism_family,
            mechanism=args.mechanism,
            gcl_hook=args.gcl_hook,
            transferable_unit=args.transferable_unit,
            non_transferable_part=args.non_transferable_part,
            fast_validation_cue=args.fast_validation_cue,
            idea_seed=args.idea_seed,
            risks=args.risks,
            next_step=args.next_step,
        ),
        encoding="utf-8",
    )
    print(f"Wrote richer paper card template to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
