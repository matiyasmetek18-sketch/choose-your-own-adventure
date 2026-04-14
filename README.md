# The Cave of Time — Choose Your Own Adventure

An interactive web app for reading and exploring *The Cave of Time*, the first-ever Choose Your Own Adventure book (1979).

## 🌐 Live Site

**[https://Christiewmy1.github.io/choose-your-own-adventure/](https://Christiewmy1.github.io/choose-your-own-adventure/)**

## 📁 GitHub Repository

**[https://github.com/Christiewmy1/choose-your-own-adventure](https://github.com/Christiewmy1/choose-your-own-adventure)**

## 👥 Team Members

- Christie Yiu
- Sio Hang Yiu
- Matiyas Dawit

---

## What It Does

This project extends the original story-extraction work by Yusuf Pisan and adds a full web-based reader:

- **Read Mode** — Play through the story interactively. Read each page, click your choices, and find one of 52 possible endings.
- **Story Map** — A live graph showing all 111 pages and their connections. Your current page is highlighted. Click any node to jump to that page.
- **Breadcrumb trail** — See every page you've visited on your current path.
- **Back & Restart** — Undo your last choice or start fresh at any time.

---

## Running Locally

### Prerequisites
- Node.js 18+
- Python 3 (for regenerating story data from source)

### Install & Run

```bash
# Clone the repo
git clone https://github.com/Christiewmy1/choose-your-own-adventure.git
cd choose-your-own-adventure

# Go into the web app folder
cd web

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Then open [http://localhost:5173/choose-your-own-adventure/](http://localhost:5173/choose-your-own-adventure/)

---

## Deploying to GitHub Pages

```bash
cd web
npm run deploy
```

This builds the app and pushes to the `gh-pages` branch automatically.

---

## Regenerating Story Data from Scratch

The story data (`web/src/story-data.json`) is pre-generated from the OCR'd text files. To regenerate it:

```bash
# First re-extract OCR pages from the PDF (if needed)
python3 scripts/reextract_cot_ocr_split.py \
  --pdf samples/the-cave-of-time.pdf \
  --pdf-start-page 8 \
  --pdf-end-page 66 \
  --story-start-page 2 \
  --output-dir output/cot-pages-ocr-v2

# Then rebuild the story graph
python3 scripts/build_story_graph.py \
  --pages-dir output/cot-pages-ocr-v2 \
  --output output/cot-story-graph.mmd

# Then regenerate story-data.json for the web app
python3 scripts/generate_story_json.py \
  --pages-dir output/cot-pages-ocr-v2 \
  --output web/src/story-data.json
```

---

## Project Structure

```
choose-your-own-adventure/
├── output/
│   ├── cot-pages-ocr-v2/     # OCR'd story pages (111 .txt files)
│   ├── cot-story-graph.mmd   # Mermaid graph of all page connections
│   ├── cot-story-graph.svg   # Visual graph (SVG)
│   └── cot-stories/          # 45 pre-written full story paths
├── scripts/                   # Python processing scripts
├── samples/                   # Original PDF
├── web/                       # React web app (this is what gets deployed)
│   ├── src/
│   │   ├── components/
│   │   │   ├── StoryReader.jsx
│   │   │   └── StoryGraph.jsx
│   │   ├── hooks/
│   │   │   └── useStory.js
│   │   ├── story-data.json    # Pre-processed story data
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
├── AI-Instructions.md         # Human-authored AI prompting log
├── Brainstorm.md              # Project ideas and planning
├── Codebase.md                # Architecture notes (updated each session)
├── Fork-Instructions.md       # Original fork instructions from Yusuf Pisan
└── ToDo.md                    # Task checklist
```

---

## Original Project

This is a fork of [Yusuf Pisan's choose-your-own-adventure](https://github.com/pisanuw/choose-your-own-adventure).
The original work extracted and processed the story data. This fork adds the interactive web interface.

---

## Tech Stack

- **React + Vite** — web app framework
- **Cytoscape.js** — story graph visualization
- **GitHub Pages** — free static hosting
- **Python 3** — story data extraction and processing