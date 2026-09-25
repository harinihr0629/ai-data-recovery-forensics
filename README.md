# AI-Assisted Data Recovery & Digital Forensics Platform

A production-style recovery workspace for investigating damaged, deleted, and fragmented digital evidence using a persistent SQLite-backed backend, modular analysis engine, and AI-assisted investigation workflow.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Features

- Persistent evidence management with SQLAlchemy + SQLite
- Synthetic demo dataset generation for damaged media and artifacts
- File identification, hashing, metadata extraction, and fragment analysis
- Integrity, recoverability, and prioritization scoring
- AI assistant with database-backed local heuristic tools
- Investigation, reporting, and audit functions
- Security-first evidence handling without destructive overwrites

## Project structure

```text
project/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── config/
├── database/
├── core/
├── ai/
├── services/
├── ui/
├── storage/
└── tests/
```
