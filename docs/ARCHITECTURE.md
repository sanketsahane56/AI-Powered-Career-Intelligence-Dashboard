# CareerIQ Technical Architecture

This document outlines the architecture, data models, and core execution flow of **CareerIQ**.

---

## 🏛️ System Architecture

```
[ Client Layer ]
    │  Browser (Vanilla JS / Chart.js / Lucide)
    │  OR Terminal (`cli.py`)
    ▼
[ Web Serving Layer ]
    │  WSGI Server: Gunicorn (Linux/Render) / Waitress (Windows)
    │  Flask Application (`app.py`)
    ▼
[ Processing Pipeline ]
    ├── 1. Document Extraction (`engine/extractor.py`)
    │       • PDF parsing via `pypdf`
    │       • Plain text normalization & cleaning
    │       • Header & contact regex heuristics
    │
    ├── 2. Analysis & Scoring Engine (`engine/analyzer.py`)
    │       • Skills Taxonomy matching (`engine/skills_taxonomy.py`)
    │       • Metric & quantifiable impact detector
    │       • Action verb & voice classifier
    │       • Role compatibility matrix evaluator
    │       • Job description gap analyzer
    │
    ├── 3. Persistence Layer (`database/db.py`)
    │       • Local SQLite database (`data/careeriq.db`)
    │       • Session storage & statistical aggregations
    │
    └── 4. PDF Reporting (`engine/report_generator.py`)
            • In-memory vector PDF generator via `reportlab`
```

---

## 📊 Database Schema (`careeriq.db`)

The SQLite database consists of an `analyses` table:

```sql
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    candidate_name TEXT,
    email TEXT,
    phone TEXT,
    overall_score INTEGER,
    top_role TEXT,
    top_domain TEXT,
    skills_count INTEGER,
    word_count INTEGER,
    analysis_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔒 Privacy & Offline Operation

- No network sockets are opened to external AI endpoints (OpenAI, Anthropic, Gemini, etc.).
- All keyword taxonomy lookups and regular expression evaluations are executed in-memory on the host machine.
