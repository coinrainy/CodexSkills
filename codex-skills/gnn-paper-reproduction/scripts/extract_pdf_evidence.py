from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

def load_reader(pdf_path: Path):
    errors: list[str] = []

    try:
        from pypdf import PdfReader as Reader  # type: ignore

        return "pypdf", Reader(str(pdf_path)), errors
    except Exception as exc:
        errors.append(f"pypdf: {exc}")

    try:
        from PyPDF2 import PdfReader as Reader  # type: ignore

        return "PyPDF2", Reader(str(pdf_path)), errors
    except Exception as exc:
        errors.append(f"PyPDF2: {exc}")

    try:
        import fitz  # type: ignore

        return "pymupdf", fitz.open(str(pdf_path)), errors
    except Exception as exc:
        errors.append(f"pymupdf: {exc}")

    raise RuntimeError("No PDF reader backend available. " + " | ".join(errors))


def iter_pages(reader_backend: str, reader, limit: int):
    if reader_backend in {"pypdf", "PyPDF2"}:
        for page_idx, page in enumerate(reader.pages[:limit], start=1):
            yield page_idx, page.extract_text() or ""
        return

    if reader_backend == "pymupdf":
        for page_idx in range(min(limit, reader.page_count)):
            yield page_idx + 1, reader.load_page(page_idx).get_text("text") or ""
        return

    raise RuntimeError(f"Unsupported reader backend: {reader_backend}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract lightweight page-level evidence from a paper PDF.")
    parser.add_argument("pdf", help="Path to the paper PDF.")
    parser.add_argument("--output", help="Optional path to write JSON output.")
    parser.add_argument("--max-pages", type=int, default=0, help="Only read the first N pages when > 0.")
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help="Case-insensitive keyword to search for. Can be provided multiple times.",
    )
    parser.add_argument("--snippet-chars", type=int, default=220, help="Snippet length around a match.")
    return parser.parse_args()


def make_snippet(text: str, index: int, width: int) -> str:
    start = max(0, index - width // 2)
    end = min(len(text), index + width // 2)
    return " ".join(text[start:end].split())


def main() -> int:
    args = parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    pdf_path = Path(args.pdf)
    try:
        reader_backend, reader, backend_errors = load_reader(pdf_path)
    except Exception as exc:
        payload = {
            "pdf": str(pdf_path),
            "status": "error",
            "error": str(exc),
            "queries": args.query,
            "results": [],
        }
        rendered = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
            print(f"Wrote PDF evidence error payload to {output_path}")
        else:
            try:
                print(rendered)
            except UnicodeEncodeError:
                sys.stdout.buffer.write(rendered.encode("utf-8", errors="replace"))
        return 1

    total_pages = len(reader.pages) if reader_backend in {"pypdf", "PyPDF2"} else reader.page_count
    limit = args.max_pages if args.max_pages > 0 else total_pages

    results: list[dict[str, object]] = []
    queries = [q.lower() for q in args.query]

    for page_idx, text in iter_pages(reader_backend, reader, limit):
        normalized = " ".join(text.split())
        page_result: dict[str, object] = {
            "page": page_idx,
            "chars": len(normalized),
        }

        if queries:
            matches = []
            lowered = normalized.lower()
            for query in queries:
                index = lowered.find(query)
                if index != -1:
                    matches.append(
                        {
                            "query": query,
                            "snippet": make_snippet(normalized, index, args.snippet_chars),
                        }
                    )
            if matches:
                page_result["matches"] = matches
                results.append(page_result)
        elif normalized:
            page_result["preview"] = normalized[: args.snippet_chars]
            results.append(page_result)

    payload = {
        "pdf": str(pdf_path),
        "status": "ok",
        "reader_backend": reader_backend,
        "reader_backend_errors": backend_errors,
        "pages_total": total_pages,
        "pages_scanned": limit,
        "queries": args.query,
        "results": results,
    }

    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote PDF evidence to {output_path}")
    else:
        try:
            print(rendered)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(rendered.encode("utf-8", errors="replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
