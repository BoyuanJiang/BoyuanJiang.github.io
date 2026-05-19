#!/usr/bin/env python3
"""Fetch Google Scholar citation counts and write homepage data files."""

from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
from pathlib import Path

from scholarly import scholarly


SCHOLAR_ID = "u62rcKoAAAAJ"

PAPERS = {
    "ifrnet": {
        "title": "IFRNet: Intermediate Feature Refine Network for Efficient Frame Interpolation",
        "year": "2022",
        "aliases": [],
    },
    "stm": {
        "title": "STM: Spatiotemporal and Motion Encoding for Action Recognition",
        "year": "2019",
        "aliases": ["STM: SpatioTemporal and Motion Encoding for Action Recognition"],
    },
}


def normalize_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", normalized.lower()).strip()


def matches_paper(scholar_title: str, paper: dict[str, object]) -> bool:
    observed = normalize_title(scholar_title)
    if "supplementary material" in observed:
        return False

    candidates = [paper["title"], *paper.get("aliases", [])]
    for candidate in candidates:
        expected = normalize_title(str(candidate))
        if observed == expected or expected in observed or observed in expected:
            return True
    return False


def empty_data() -> dict[str, object]:
    return {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "scholar_id": SCHOLAR_ID,
        "total_citations": None,
        "h_index": None,
        "i10_index": None,
        "papers": {
            key: {
                "title": paper["title"],
                "citations": None,
                "year": paper["year"],
                "url": "",
            }
            for key, paper in PAPERS.items()
        },
    }


def fetch_scholar_data() -> dict[str, object]:
    print(f"Fetching Google Scholar profile: {SCHOLAR_ID}")
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author)

    data = empty_data()
    data["total_citations"] = author.get("citedby", 0)
    data["h_index"] = author.get("hindex", 0)
    data["i10_index"] = author.get("i10index", 0)

    for publication in author.get("publications", []):
        title = publication.get("bib", {}).get("title", "")
        if not title:
            continue

        for key, paper in PAPERS.items():
            if not matches_paper(title, paper):
                continue

            citations = int(publication.get("num_citations", 0) or 0)
            current = data["papers"][key]["citations"]
            if current is None or citations > int(current):
                data["papers"][key] = {
                    "title": title,
                    "citations": citations,
                    "year": publication.get("bib", {}).get("pub_year", paper["year"]),
                    "url": publication.get("author_pub_id", ""),
                }
                print(f"  {key}: {citations} citations")
            break

    return data


def write_data_files(data: dict[str, object]) -> None:
    root = Path(__file__).resolve().parents[1]
    json_path = root / "_data" / "citations.json"
    js_path = root / "assets" / "js" / "citations-data.js"

    json_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.parent.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(data, indent=2, ensure_ascii=False)
    json_path.write_text(f"{json_text}\n", encoding="utf-8")
    js_path.write_text(f"window.__CITATION_DATA__ = {json_text};\n", encoding="utf-8")

    print(f"Wrote {json_path.relative_to(root)}")
    print(f"Wrote {js_path.relative_to(root)}")


def main() -> int:
    try:
        data = fetch_scholar_data()
    except Exception as error:
        print(f"Failed to fetch Google Scholar citations: {error}", file=sys.stderr)
        return 1

    write_data_files(data)
    tracked = sum(1 for paper in data["papers"].values() if paper["citations"] is not None)
    print(f"Tracked papers with citations: {tracked}/{len(PAPERS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
