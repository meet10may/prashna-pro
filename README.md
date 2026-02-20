# PrashnaPro — प्रश्नप्रो

AI tool that converts photos of handwritten papers into structured, polished, print-ready exam documents automatically.

## Features

- **OCR with GPT-4o Vision** — Upload photos of handwritten question papers, AI extracts all text
- **Full visual editor** — Edit every question, marks, options, instructions before generating
- **Hindi support** — Built-in Hindi transliteration tool (type English → get Hindi)
- **Match-the-following** — Auto-detects and formats two-column tables
- **MCQ optimization** — 2×2 grid layout for multiple choice options
- **Compact mode** — Reduces margins and spacing to save paper
- **Professional .docx output** — School logo, header, sections, page numbers

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Enter your OpenAI API key in the toolbar, upload handwritten paper images, and generate.

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path: `app.py`
5. Deploy

## Tech Stack

- Streamlit (UI)
- OpenAI GPT-4o Vision (OCR)
- python-docx (document generation)

## License

MIT
