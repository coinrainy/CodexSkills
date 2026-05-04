from __future__ import annotations

import argparse
import json
from pathlib import Path


MASTER_HEADER = (
    "canonical_id,title,year,venue,track,bucket,relevance,primary_url,code_url,"
    "discovered_on,last_reviewed_on,dedup_key,status,local_card_path,notion_page_id,"
    "weekly_digest,duplicate_of,notes\n"
)

QUERY_LOG_TEMPLATE = """# 检索日志

按周记录你实际用过的检索词、检索源、筛选标准和本周新增论文数。

## {week_label}

- 检索时间：
- 检索源：
- 关键词：
- 顶会顶刊范围：
- 新增论文数：
- 直接相关：
- 可迁移相关：
- 重复跳过：
- 备注：
"""

NOTION_TEMPLATE = {
    "papers_data_source_id": "REPLACE_ME",
    "weekly_digest_page_id": "REPLACE_ME",
    "title_property": "Title",
    "canonical_id_property": "Canonical ID",
    "url_property": "Paper URL",
    "status_property": "Status",
    "tags_property": "Tags",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize literature pipeline workspace.")
    parser.add_argument(
        "--root",
        default=".",
        help="Workspace root where literature_pipeline will be created.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite template files.")
    parser.add_argument(
        "--week-label",
        default="YYYY-WW",
        help="Default week label inserted into query_log.md.",
    )
    return parser.parse_args()


def write_if_needed(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    pipeline = root / "literature_pipeline"

    created: list[Path] = []
    for subdir in ("state", "paper_cards", "weekly_digests", "notion_import"):
        path = pipeline / subdir
        path.mkdir(parents=True, exist_ok=True)

    if write_if_needed(pipeline / "state" / "master_papers.csv", MASTER_HEADER, args.force):
        created.append(pipeline / "state" / "master_papers.csv")
    if write_if_needed(
        pipeline / "state" / "query_log.md",
        QUERY_LOG_TEMPLATE.format(week_label=args.week_label),
        args.force,
    ):
        created.append(pipeline / "state" / "query_log.md")
    if write_if_needed(
        pipeline / "state" / "notion_config.template.json",
        json.dumps(NOTION_TEMPLATE, ensure_ascii=False, indent=2) + "\n",
        args.force,
    ):
        created.append(pipeline / "state" / "notion_config.template.json")

    for keep_path in (
        pipeline / "paper_cards" / ".gitkeep",
        pipeline / "weekly_digests" / ".gitkeep",
        pipeline / "notion_import" / ".gitkeep",
    ):
        if write_if_needed(keep_path, "", args.force):
            created.append(keep_path)

    print(f"Initialized literature pipeline under {pipeline}")
    if created:
        print("Created files:")
        for path in created:
            print(f"- {path}")
    else:
        print("No files created. Use --force to overwrite templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
