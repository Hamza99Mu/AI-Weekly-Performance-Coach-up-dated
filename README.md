# AI Weekly Performance Coach

A modular Streamlit app that audits a past week and creates an actionable plan for the upcoming week.

## Features

- Paste weekly activities
- Upload DOCX
- Structured JSON output
- Overall score
- Goal progress
- Potentially recoverable time
- Time eaters
- Weekly Audit
- Keep Going / Good / Best
- Next-week priorities
- Final result
- JSON download

## Files

- `app.py` — Streamlit UI
- `analyzer.py` — DOCX extraction, Groq API, JSON parsing and validation
- `prompts.py` — AI instructions and JSON contract
- `requirements.txt` — dependencies
- `.env.example` — environment template
- `.gitignore` — secret/local files
- `README.md` — documentation

## Model

Uses Groq with:

`openai/gpt-oss-120b`

The API call uses JSON mode:

`response_format={"type": "json_object"}`

This is the key fix for malformed JSON errors such as:

`Expecting ',' delimiter`

## Setup

Use Python 3.10+.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```text
GROQ_API_KEY=your_real_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Run:

```bash
streamlit run app.py
```

Then open the URL shown by Streamlit, normally `http://localhost:8501`.

## Recommended input

Use:

`Task — time — status`

Example:

```text
Thesis research — 2 hours — completed
Python learning — 1.5 hours — completed
YouTube — 2 hours
Client work — 3 hours — completed
```

## Architecture

User → `app.py` → `analyzer.py` → Groq → validated JSON → Streamlit dashboard

Python handles extraction, API communication, JSON parsing, validation, calculations and UI.

AI handles interpretation, audit, time-eater reasoning, insights and next-week recommendations.

## Security

Never commit `.env` or put the API key in source code.
