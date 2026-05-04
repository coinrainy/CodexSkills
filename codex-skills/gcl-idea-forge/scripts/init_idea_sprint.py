from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


WEEK_ID_PATTERN = re.compile(r"(\d{4}-W\d{2})")
SPRINT_CARD_PATTERN = re.compile(r"- card:\s*`([^`]+)`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a Markdown template for a paper-batch GCL idea sprint. "
            "By default, it uses the latest weekly digest and selects papers "
            "from that week that have not appeared in previous idea sprints."
        )
    )
    parser.add_argument("output", nargs="?", help="Optional output Markdown path.")
    parser.add_argument("--topic", default=None, help="Optional sprint topic.")
    parser.add_argument(
        "--digest",
        default=None,
        help="Digest path, filename, or week id such as 2026-W19. Defaults to latest digest.",
    )
    parser.add_argument(
        "--goal",
        default="从新论文批次中提炼 3 到 5 个可执行的 GCL idea",
        help="Main brainstorming goal.",
    )
    parser.add_argument(
        "--paper-card",
        action="append",
        default=[],
        help="Explicit paper card path. Repeat for multiple cards.",
    )
    parser.add_argument(
        "--include-covered",
        action="store_true",
        help="Include papers that already appeared in older idea sprints for the same week.",
    )
    parser.add_argument(
        "--backlog-prefix",
        default="gcl",
        help="Short prefix for generated backlog ids.",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite the output file if it exists."
    )
    return parser.parse_args()


def find_workspace_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "literature_pipeline").exists():
            return candidate
    raise SystemExit(
        "Could not locate workspace root with literature_pipeline/. "
        "Run this script inside the target repository."
    )


def normalize_rel_path(path: Path, workspace_root: Path) -> str:
    try:
        rel_path = path.relative_to(workspace_root)
    except ValueError:
        rel_path = path
    return rel_path.as_posix()


def extract_week_id(value: str) -> str | None:
    match = WEEK_ID_PATTERN.search(value)
    if match:
        return match.group(1)
    return None


def resolve_digest_path(
    digest_arg: str | None, workspace_root: Path, weekly_digest_dir: Path
) -> Path:
    if digest_arg:
        direct = Path(digest_arg)
        candidates = []
        if direct.is_absolute():
            candidates.append(direct)
        else:
            candidates.extend(
                [
                    workspace_root / digest_arg,
                    weekly_digest_dir / digest_arg,
                ]
            )
            week_id = extract_week_id(digest_arg)
            if week_id:
                candidates.append(weekly_digest_dir / f"{week_id}.md")

        for candidate in candidates:
            if candidate.exists():
                return candidate
        raise SystemExit(f"Digest not found: {digest_arg}")

    digest_files = sorted(
        [path for path in weekly_digest_dir.glob("*.md") if path.name != ".gitkeep"]
    )
    if not digest_files:
        raise SystemExit("No weekly digests found under literature_pipeline/weekly_digests.")
    return digest_files[-1]


def resolve_card_path(card_arg: str, workspace_root: Path) -> Path:
    card_path = Path(card_arg)
    if card_path.is_absolute():
        return card_path
    return workspace_root / card_path


def extract_field(text: str, label: str) -> str | None:
    pattern = rf"-\s*{re.escape(label)}[:：]\s*(.+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None


def clean_value(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    return value.strip().strip("`")


def summarize_card(card_path: Path) -> dict[str, str]:
    try:
        text = card_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {
            "title": card_path.stem,
            "relation": "TBD",
            "relevance_judgment": "TBD",
            "bottleneck": "TBD",
            "mechanism_family": "TBD",
            "mechanism": "TBD",
            "gcl_hook": "TBD",
            "transfer": "TBD",
            "non_transferable": "TBD",
            "fast_validation_cue": "TBD",
            "idea_seed": "TBD",
        }

    return {
        "title": clean_value(extract_field(text, "标题"), card_path.stem),
        "relation": clean_value(
            extract_field(text, "与 GCL 的关系") or extract_field(text, "和 GCL 的关系"),
            "TBD",
        ),
        "relevance_judgment": clean_value(extract_field(text, "相关性判断"), "TBD"),
        "bottleneck": clean_value(extract_field(text, "目标瓶颈"), "TBD"),
        "mechanism_family": clean_value(extract_field(text, "机制类别"), "TBD"),
        "mechanism": clean_value(extract_field(text, "核心机制"), "TBD"),
        "gcl_hook": clean_value(extract_field(text, "GCL 挂接点"), "TBD"),
        "transfer": clean_value(extract_field(text, "可迁移点"), "TBD"),
        "non_transferable": clean_value(extract_field(text, "不可直接迁移部分"), "TBD"),
        "fast_validation_cue": clean_value(extract_field(text, "最快验证线索"), "TBD"),
        "idea_seed": clean_value(extract_field(text, "Idea seed"), "TBD"),
    }


def collect_weekly_cards(master_csv_path: Path, week_id: str, workspace_root: Path) -> list[Path]:
    cards: list[Path] = []
    with master_csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("weekly_digest") != week_id:
                continue
            raw_path = (row.get("local_card_path") or "").strip()
            if not raw_path:
                continue
            card_path = resolve_card_path(raw_path, workspace_root)
            if card_path.exists():
                cards.append(card_path)
    return cards


def collect_covered_cards(
    idea_sprint_dir: Path, week_id: str, workspace_root: Path
) -> set[str]:
    covered_cards: set[str] = set()
    for sprint_path in sorted(idea_sprint_dir.glob(f"{week_id}-gcl-idea-sprint*.md")):
        text = sprint_path.read_text(encoding="utf-8")
        for match in SPRINT_CARD_PATTERN.finditer(text):
            card_path = resolve_card_path(match.group(1), workspace_root)
            covered_cards.add(normalize_rel_path(card_path, workspace_root))
    return covered_cards


def infer_selected_cards(
    args: argparse.Namespace,
    workspace_root: Path,
    weekly_cards: list[Path],
    covered_cards: set[str],
) -> tuple[list[Path], str]:
    if args.paper_card:
        selected_cards = [resolve_card_path(item, workspace_root) for item in args.paper_card]
        return selected_cards, "显式指定的论文卡"

    if args.include_covered:
        return weekly_cards, "本周全部论文卡（含已进入旧 sprint 的论文）"

    selected_cards = [
        card
        for card in weekly_cards
        if normalize_rel_path(card, workspace_root) not in covered_cards
    ]
    return selected_cards, "本周新增且尚未进入 idea sprint 的论文卡"


def next_sprint_index(idea_sprint_dir: Path, week_id: str) -> int:
    pattern = re.compile(rf"^{re.escape(week_id)}-gcl-idea-sprint(?:-(\d{{2}}))?\.md$")
    max_index = 0
    for sprint_path in idea_sprint_dir.glob(f"{week_id}-gcl-idea-sprint*.md"):
        match = pattern.match(sprint_path.name)
        if not match:
            continue
        if match.group(1):
            max_index = max(max_index, int(match.group(1)))
        else:
            max_index = max(max_index, 1)
    return max_index + 1 if max_index else 1


def build_output_path(
    output_arg: str | None, idea_sprint_dir: Path, week_id: str
) -> tuple[Path, int]:
    if output_arg:
        output_path = Path(output_arg)
        if not output_path.is_absolute():
            output_path = idea_sprint_dir.parent.parent / output_path
        sprint_index = next_sprint_index(idea_sprint_dir, week_id)
        explicit_index = re.search(r"-gcl-idea-sprint-(\d{2})\.md$", output_path.name)
        if explicit_index:
            sprint_index = int(explicit_index.group(1))
        return output_path, sprint_index

    sprint_index = next_sprint_index(idea_sprint_dir, week_id)
    return idea_sprint_dir / f"{week_id}-gcl-idea-sprint-{sprint_index:02d}.md", sprint_index


def build_backlog_id(backlog_prefix: str, sprint_id: str, rank: int) -> str:
    return f"{backlog_prefix}-{sprint_id}-idea-{rank:02d}"


def build_card_section(selected_cards: list[Path], workspace_root: Path) -> str:
    if not selected_cards:
        return "- 当前没有可纳入的 selected paper cards\n"

    lines = []
    for card in selected_cards:
        info = summarize_card(card)
        lines.append(
            f"- `{info['title']}`\n"
            f"  - card: `{normalize_rel_path(card, workspace_root)}`\n"
            f"  - relation: {info['relation']}\n"
            f"  - relevance judgment: {info['relevance_judgment']}\n"
            f"  - bottleneck: {info['bottleneck']}\n"
            f"  - mechanism family: {info['mechanism_family']}\n"
            f"  - mechanism: {info['mechanism']}\n"
            f"  - gcl hook: {info['gcl_hook']}\n"
            f"  - transferable unit: {info['transfer']}\n"
            f"  - non-transferable part: {info['non_transferable']}\n"
            f"  - fast validation cue: {info['fast_validation_cue']}\n"
            f"  - idea seed: {info['idea_seed']}"
        )
    return "\n".join(lines) + "\n"


TEMPLATE = """# GCL Idea Sprint

## 批次概览

- sprint_id：`{sprint_id}`
- 主题：{topic}
- digest：`{digest}`
- 目标：{goal}
- 论文来源模式：{selection_mode}
- backlog 命名规则：`{backlog_prefix}-{sprint_id}-idea-01`
- selected_paper_count：{selected_paper_count}

## 已选论文信号

{paper_signal_block}

## 论文理解与证据链

| Paper | Card | Bottleneck targeted | Core mechanism | Transferable unit | Non-transferable part or caveat |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 机制归纳表

| Paper or combo | Bottleneck targeted | Mechanism | GCL integration hook | Confidence |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Idea 排序表

| Rank | Backlog ID | Idea | Source papers | Risk | Expected gain | Cost | Fastest experiment | Gate status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `{idea_1_backlog_id}` |  |  | low-risk / mid-risk / high-risk |  |  |  | pass / revise / reject |
| 2 | `{idea_2_backlog_id}` |  |  | low-risk / mid-risk / high-risk |  |  |  | pass / revise / reject |
| 3 | `{idea_3_backlog_id}` |  |  | low-risk / mid-risk / high-risk |  |  |  | pass / revise / reject |

## Shortlist 过滤规则

- 如果某个候选 idea 说不清来源论文、迁移机制、最小实现路径、最快验证实验、关键 ablation、stop condition，就不要保留在 shortlist 中。
- 如果某个候选 idea 需要大规模 sweep 才有可能成立，默认标记为 `revise` 或 `reject`，而不是直接进前 3。
- 如果某个候选 idea 没有明确代码挂接点，先降级，不要包装成高优先级方向。

## 重点 Idea 卡片

### Idea 1

- Backlog ID：`{idea_1_backlog_id}`
- Gate status：pass / revise / reject
- 一句话主张：
- 来源论文：
- 来源 card：
- 为什么这些论文可以组合：
- 论文级证据链：
  - Paper A bottleneck：
  - Paper A mechanism：
  - Paper A transferable unit：
  - Paper A non-transferable part：
  - Paper B bottleneck：
  - Paper B mechanism：
  - Paper B transferable unit：
  - Paper B non-transferable part：
- 为什么对当前 GCL 可能有效：
- 最小实现路径：
- 最快验证实验：
- 关键 ablation：
- 主要失败模式：
- Stop condition：
- 最不确定的地方：
- Feasibility gate：
  - 至少 1 篇 direct GCL 论文：yes / no
  - 代码挂接点已明确：yes / no
  - 1 到 3 天内可完成 smoke experiment：yes / no
  - 至少 1 个必要 ablation：yes / no
  - 不依赖大规模 sweep 才能成立：yes / no

### Idea 2

- Backlog ID：`{idea_2_backlog_id}`
- Gate status：pass / revise / reject
- 一句话主张：
- 来源论文：
- 来源 card：
- 为什么这些论文可以组合：
- 论文级证据链：
  - Paper A bottleneck：
  - Paper A mechanism：
  - Paper A transferable unit：
  - Paper A non-transferable part：
  - Paper B bottleneck：
  - Paper B mechanism：
  - Paper B transferable unit：
  - Paper B non-transferable part：
- 为什么对当前 GCL 可能有效：
- 最小实现路径：
- 最快验证实验：
- 关键 ablation：
- 主要失败模式：
- Stop condition：
- 最不确定的地方：
- Feasibility gate：
  - 至少 1 篇 direct GCL 论文：yes / no
  - 代码挂接点已明确：yes / no
  - 1 到 3 天内可完成 smoke experiment：yes / no
  - 至少 1 个必要 ablation：yes / no
  - 不依赖大规模 sweep 才能成立：yes / no

### Idea 3

- Backlog ID：`{idea_3_backlog_id}`
- Gate status：pass / revise / reject
- 一句话主张：
- 来源论文：
- 来源 card：
- 为什么这些论文可以组合：
- 论文级证据链：
  - Paper A bottleneck：
  - Paper A mechanism：
  - Paper A transferable unit：
  - Paper A non-transferable part：
  - Paper B bottleneck：
  - Paper B mechanism：
  - Paper B transferable unit：
  - Paper B non-transferable part：
- 为什么对当前 GCL 可能有效：
- 最小实现路径：
- 最快验证实验：
- 关键 ablation：
- 主要失败模式：
- Stop condition：
- 最不确定的地方：
- Feasibility gate：
  - 至少 1 篇 direct GCL 论文：yes / no
  - 代码挂接点已明确：yes / no
  - 1 到 3 天内可完成 smoke experiment：yes / no
  - 至少 1 个必要 ablation：yes / no
  - 不依赖大规模 sweep 才能成立：yes / no

## Rejected Or Deferred Ideas

- 候选方向：
  - 为什么先不做：
  - 如果以后重启，需要补什么证据：

## 推荐执行顺序

1. 
2. 
3. 

## 不建议优先投入的方向

- 

## 下一步建议

- 先补读哪些论文：
- 先跑哪个最小实验：
- 什么结果出现后值得扩大 sweep：
"""


def main() -> int:
    args = parse_args()
    workspace_root = find_workspace_root(Path.cwd())
    literature_root = workspace_root / "literature_pipeline"
    weekly_digest_dir = literature_root / "weekly_digests"
    idea_sprint_dir = literature_root / "idea_sprints"
    master_csv_path = literature_root / "state" / "master_papers.csv"

    digest_path = resolve_digest_path(args.digest, workspace_root, weekly_digest_dir)
    week_id = extract_week_id(digest_path.name)
    if not week_id:
        raise SystemExit(f"Could not infer week id from digest: {digest_path}")

    weekly_cards = collect_weekly_cards(master_csv_path, week_id, workspace_root)
    covered_cards = collect_covered_cards(idea_sprint_dir, week_id, workspace_root)
    selected_cards, selection_mode = infer_selected_cards(
        args, workspace_root, weekly_cards, covered_cards
    )

    if not selected_cards:
        raise SystemExit(
            f"No uncovered paper cards found for {week_id}. "
            "Use --include-covered or --paper-card to override."
        )

    output_path, sprint_index = build_output_path(args.output, idea_sprint_dir, week_id)
    if output_path.exists() and not args.force:
        raise SystemExit(f"{output_path} already exists. Re-run with --force to overwrite.")

    sprint_id = f"{week_id}-gcl-idea-sprint-{sprint_index:02d}"
    topic = args.topic or f"{week_id} GCL paper batch"
    paper_signal_block = build_card_section(selected_cards, workspace_root)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        TEMPLATE.format(
            sprint_id=sprint_id,
            topic=topic,
            digest=normalize_rel_path(digest_path, workspace_root),
            goal=args.goal,
            selection_mode=selection_mode,
            backlog_prefix=args.backlog_prefix,
            selected_paper_count=len(selected_cards),
            paper_signal_block=paper_signal_block,
            idea_1_backlog_id=build_backlog_id(args.backlog_prefix, sprint_id, 1),
            idea_2_backlog_id=build_backlog_id(args.backlog_prefix, sprint_id, 2),
            idea_3_backlog_id=build_backlog_id(args.backlog_prefix, sprint_id, 3),
        ),
        encoding="utf-8",
    )
    print(f"Wrote idea sprint template to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
