# Codebase Notes

_Last updated: April 2026 — Christie Yiu, Sio Hang Yiu, Matiyas Dawit_

---

## Purpose

This project has two parts:

1. **Data pipeline** (original work by Yusuf Pisan) — extracts text from the scanned PDF of *The Cave of Time*, builds a story graph, and writes all possible bounded story paths.
2. **Web app** (added by this fork) — an interactive React app for reading the story and visualizing the story graph.

---

## Read This First

- The canonical extracted page set is `output/cot-pages-ocr-v2/`
- Do NOT use the older `cot-pages` extraction. It had bad OCR and was deleted.
- The web app lives in `web/` and is deployed to GitHub Pages.
- Story data for the web app is pre-processed into `web/src/story-data.json`

---

## Important PDF Mapping

The scan is a two-page spread layout:
- PDF page 8 → story page 2 (left) and story page 3 (right)
- PDF page 9 → story page 4 (left) and story page 5 (right)

Story starts on page 2: *"You've hiked through Snake Canyon once before..."*

Do not confuse story page numbers with PDF page numbers.

---

## Data Pipeline Scripts (`scripts/`)

| Script | What it does |
|--------|-------------|
| `reextract_cot_ocr_split.py` | Re-extracts story pages from PDF using OCR on left/right halves of each spread |
| `build_story_graph.py` | Builds Mermaid graph from OCR pages |
| `write_all_stories.py` | Writes all bounded story paths (max 20 decisions, no loops) |
| `render_story_graph_svg.py` | Renders the Mermaid graph to SVG |
| `generate_story_json.py` | *(new)* Exports story data to `web/src/story-data.json` for the web app |

Superseded scripts (deleted): `extract_cot.py`, `reextract_cot_spreads.py`

---

## Web App (`web/`)

### Tech Stack
- React 19 + Vite 8
- Cytoscape.js (story graph)
- GitHub Pages (deployment via `gh-pages` package)

### Key Files

```
web/
├── src/
│   ├── story-data.json         # Pre-processed story: all pages, choices, graph edges
│   ├── App.jsx                 # Root component, layout (reader + graph panels)
│   ├── App.css                 # All styles (dark theme)
│   ├── hooks/
│   │   └── useStory.js         # State: currentPage, history, goToPage, goBack, restart
│   └── components/
│       ├── StoryReader.jsx     # Displays page text, choices, breadcrumb, ending screen
│       └── StoryGraph.jsx      # Cytoscape interactive graph, highlights current page
├── vite.config.js              # base: '/choose-your-own-adventure/' for GitHub Pages
└── package.json                # deploy script: npm run deploy → gh-pages -d dist
```

### story-data.json Format

```json
{
  "startPage": 2,
  "pages": {
    "2": {
      "id": 2,
      "text": "You've hiked through Snake Canyon...",
      "choices": [
        { "text": "If you decide to start back home, turn to page 4", "page": 4 },
        { "text": "If you decide to wait, turn to page 5", "page": 5 }
      ],
      "isTerminal": false,
      "isContinuation": false
    }
  }
}
```

- `isTerminal: true` — page has no choices (story ending), shown as red node
- `isContinuation: true` — page text flows into next sequential page (OCR split artifact), shown as purple node

### Node Colors in Graph
- 🟢 Green — start page (page 2)
- ⚫ Gray — normal pages
- 🔴 Red — terminal/ending pages (52 total)
- 🟣 Purple — continuation pages (text splits across PDF spread)
- 🟡 Yellow — your current page

---

## Canonical Outputs

Keep these:
- `output/cot-pages-ocr-v2/` — 111 story page text files
- `output/cot-story-graph.mmd` — Mermaid graph
- `output/cot-story-graph.svg` — Visual SVG graph
- `output/cot-stories/` — 45 pre-written story paths
- `web/src/story-data.json` — Processed data for web app

Deleted (obsolete):
- `output/cot-pages/`
- `output/cot-pages-reextract/`
- `output/cot-stories-from-page-02/`
- `output/cot-stories-start10/`
- `output/tmp/`

---

## Deployment

The web app deploys to GitHub Pages:

```bash
cd web
npm run deploy
```

Live URL: `https://Christiewmy1.github.io/choose-your-own-adventure/`

---

## Known Caveats

- OCR is improved but not perfect — some pages have minor noise (e.g. "tum" for "turn", stray characters)
- The JSON parser handles the "tum/turn" OCR variant
- Pages 2 and 3 are a continuation pair (page 2 text is cut off mid-sentence, flows into page 3)
- 13 pages are marked as continuations for the same reason

## Next-Time Guidance

When resuming work:
1. Read this file first.
2. `output/cot-pages-ocr-v2/` is the source of truth for story text.
3. Web app is in `web/` — run `npm install && npm run dev` to start locally.
4. If story data needs regeneration, run `generate_story_json.py` then rebuild the web app.
5. To deploy: `cd web && npm run deploy`