#!/usr/bin/env python3
"""
generate_story_json.py

Parses output/cot-pages-ocr-v2/*.txt files and produces
web/src/story-data.json for the React web app.

Usage:
    python3 scripts/generate_story_json.py
    python3 scripts/generate_story_json.py \
        --pages-dir output/cot-pages-ocr-v2 \
        --output web/src/story-data.json
"""

import re
import json
import argparse
from pathlib import Path


def parse_choices(text):
    """Extract choices from page text, handling OCR variants of 'turn'."""
    choices = []
    pattern = (
        r'(If[^\n]{0,120}?(?:turn|tum|tu\s*m)\s+to\s+page\s+(\d+)'
        r'|(?:turn|tum|Tu\s*m|Turn|Tum)\s+to\s+page\s+(\d+))'
    )
    for m in re.finditer(pattern, text, re.IGNORECASE):
        dest = m.group(2) or m.group(3)
        label = m.group(0).strip().rstrip('.')
        choices.append({"text": label, "page": int(dest)})
    return choices


def load_pages(pages_dir):
    pages = {}
    for path in sorted(Path(pages_dir).glob("*.txt")):
        match = re.match(r'^(\d+)-CoT\.txt$', path.name)
        if not match:
            continue
        page_num = int(match.group(1))
        text = path.read_text(encoding='utf-8', errors='replace')
        # Strip leading "Page N" header
        text = re.sub(r'^Page \d+\s*\n+', '', text).strip()
        pages[page_num] = text
    return pages


def build_story_data(pages_dir, start_page=2):
    pages = load_pages(pages_dir)
    all_page_nums = sorted(pages.keys())

    # Find all pages that are destinations (have incoming edges)
    all_destinations = set()
    for pn in all_page_nums:
        for c in parse_choices(pages[pn]):
            all_destinations.add(c['page'])

    result = {}
    for pn in all_page_nums:
        text = pages[pn]
        choices = parse_choices(text)

        # Detect continuation pages: no choices AND not referenced by any other page
        idx = all_page_nums.index(pn)
        next_pn = all_page_nums[idx + 1] if idx + 1 < len(all_page_nums) else None
        is_continuation = (
            len(choices) == 0
            and pn not in all_destinations
            and next_pn is not None
        )

        if is_continuation:
            choices = [{"text": "Continue...", "page": next_pn}]

        result[str(pn)] = {
            "id": pn,
            "text": text,
            "choices": choices,
            "isTerminal": len(choices) == 0,
            "isContinuation": is_continuation,
        }

    terminals = [p for p in result.values() if p['isTerminal']]
    continuations = [p for p in result.values() if p['isContinuation']]
    print(f"Pages: {len(result)}  |  Endings: {len(terminals)}  |  Continuations: {len(continuations)}")

    return {"startPage": start_page, "pages": result}


def main():
    parser = argparse.ArgumentParser(description="Generate story-data.json for the web app")
    parser.add_argument('--pages-dir', default='output/cot-pages-ocr-v2',
                        help='Directory containing NN-CoT.txt files')
    parser.add_argument('--output', default='web/src/story-data.json',
                        help='Output JSON file path')
    parser.add_argument('--start-page', type=int, default=2,
                        help='Starting page number (default: 2)')
    args = parser.parse_args()

    story_data = build_story_data(args.pages_dir, args.start_page)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, indent=2, ensure_ascii=False)

    print(f"Saved → {output_path}")


if __name__ == '__main__':
    main()