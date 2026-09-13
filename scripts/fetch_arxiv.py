#!/usr/bin/env python3
"""
Récupère les papiers arXiv soumis/mis à jour dans les dernières `HOURS`
heures, pour les catégories listées dans data/topics.md.

Usage:
    python scripts/fetch_arxiv.py [--hours 24] [--max 50]

Sortie: JSON sur stdout, une liste d'objets {title, authors, abstract, link,
categories, published}. L'agent (Claude) lit cette sortie et décide
lui-même lesquels sont pertinents — ce script ne fait AUCUN filtrage
sémantique, juste une récupération brute par catégorie.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"

TOPICS_FILE = Path(__file__).resolve().parent.parent / "data" / "topics.md"


def load_categories(topics_path: Path) -> list[str]:
    text = topics_path.read_text(encoding="utf-8")
    section = text.split("## Catégories arXiv à surveiller", 1)[-1]
    section = section.split("##", 1)[0]
    return [line.strip("- ").strip() for line in section.splitlines() if line.strip().startswith("-")]


def fetch_one_category(category: str, max_results: int) -> list[dict]:
    # arXiv's API intermittently 429s/times out on multi-category "OR" queries
    # (observed consistently even for a single "+OR+"), but per-category
    # queries succeed reliably. Fetch each category separately and merge.
    url = (
        f"{ARXIV_API}?search_query=cat:{category}"
        f"&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        raw = resp.read()

    root = ET.fromstring(raw)
    papers = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        title = entry.findtext(f"{ATOM_NS}title", default="").strip()
        title = re.sub(r"\s+", " ", title)
        abstract = entry.findtext(f"{ATOM_NS}summary", default="").strip()
        abstract = re.sub(r"\s+", " ", abstract)
        published = entry.findtext(f"{ATOM_NS}published", default="")
        link = ""
        for l in entry.findall(f"{ATOM_NS}link"):
            if l.get("type") == "text/html":
                link = l.get("href", "")
        authors = [
            a.findtext(f"{ATOM_NS}name", default="")
            for a in entry.findall(f"{ATOM_NS}author")
        ]
        cats = [c.get("term") for c in entry.findall("{http://arxiv.org/schemas/atom}category")]

        papers.append(
            {
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "link": link,
                "published": published,
                "categories": cats,
            }
        )
    return papers


def fetch(categories: list[str], max_results: int) -> list[dict]:
    seen_links = set()
    papers = []
    for i, category in enumerate(categories):
        if i > 0:
            time.sleep(3)  # be polite to arXiv's API between requests
        for p in fetch_one_category(category, max_results):
            if p["link"] in seen_links:
                continue
            seen_links.add(p["link"])
            papers.append(p)
    papers.sort(key=lambda p: p["published"], reverse=True)
    return papers


def filter_by_hours(papers: list[dict], hours: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out = []
    for p in papers:
        try:
            dt = datetime.strptime(p["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if dt >= cutoff:
            out.append(p)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--max", type=int, default=100)
    args = parser.parse_args()

    categories = load_categories(TOPICS_FILE)
    if not categories:
        print("[]")
        sys.exit(0)

    papers = fetch(categories, args.max)
    recent = filter_by_hours(papers, args.hours)
    print(json.dumps(recent, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
