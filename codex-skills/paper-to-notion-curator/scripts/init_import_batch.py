from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Notion import batch from master_papers.csv.")
    parser.add_argument("--root", default=".", help="Workspace root containing literature_pipeline.")
    parser.add_argument(
        "--statuses",
        default="new,triaged",
        help="Comma separated statuses to include.",
    )
    parser.add_argument(
        "--digest",
        default="",
        help="Optional weekly digest label to filter, such as 2026-W18.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output markdown path. Defaults to literature_pipeline/notion_import/import-batch-YYYY-MM-DD.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    state_csv = root / "literature_pipeline" / "state" / "master_papers.csv"
    if not state_csv.exists():
        raise SystemExit(f"Missing state file: {state_csv}")

    wanted_statuses = {item.strip() for item in args.statuses.split(",") if item.strip()}
    rows: list[dict[str, str]] = []
    with state_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("status", "").strip() not in wanted_statuses:
                continue
            if row.get("notion_page_id", "").strip():
                continue
            if args.digest and row.get("weekly_digest", "").strip() != args.digest:
                continue
            rows.append(row)

    output = (
        Path(args.output).resolve()
        if args.output
        else root
        / "literature_pipeline"
        / "notion_import"
        / f"import-batch-{date.today().isoformat()}.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Notion 导入批次",
        "",
        f"- 来源：`{state_csv}`",
        f"- 待导入数量：{len(rows)}",
        f"- 过滤状态：{', '.join(sorted(wanted_statuses)) or 'none'}",
        f"- 周报过滤：{args.digest or 'none'}",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"## {index}. {row.get('title', 'Untitled')}",
                "",
                f"- canonical_id: `{row.get('canonical_id', '')}`",
                f"- venue: {row.get('venue', '')}",
                f"- year: {row.get('year', '')}",
                f"- track: {row.get('track', '')}",
                f"- relevance: {row.get('relevance', '')}",
                f"- primary_url: {row.get('primary_url', '')}",
                f"- local_card_path: {row.get('local_card_path', '')}",
                f"- weekly_digest: {row.get('weekly_digest', '')}",
                f"- notes: {row.get('notes', '')}",
                "",
            ]
        )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote import batch to {output}")
    print(f"Included {len(rows)} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
