# SoulLense AI

A full-stack psycholinguistic analysis platform that detects emotional patterns and manipulation dynamics in text using LLM-based classification.

**Live demo:** [soul-lenseai-x2bz.vercel.app](https://soul-lenseai-x2bz.vercel.app)
**API docs:** [soul-lenseai.onrender.com/docs](https://soul-lenseai.onrender.com/docs)

> Note: the backend is hosted on Render's free tier, which spins down after inactivity. The first request after idle time may take ~30 seconds to respond.

## Overview

SoulLense AI analyzes text input to surface emotional tone, sentiment, communication style, and manipulation patterns such as guilt-tripping, gaslighting, and emotional blackmail. It supports single-message analysis as well as two-party relationship and conversation analysis, with a dashboard for tracking trends over time.

## Features

- **Emotion Analysis** — detects emotion, sentiment, communication style, and underlying emotional needs from text
- **Manipulation Detection** — classifies nine manipulation patterns (guilt tripping, emotional blackmail, gaslighting, love bombing, and more) with toxicity scoring and risk levels
- **Relationship Analysis** — compares two participants in a conversation to identify the primary influencer and dynamic
- **Conversation Analysis** — summarizes full multi-turn exchanges and flags escalation patterns
- **History & Dashboard** — persists past analyses and surfaces aggregate stats like most common emotion and manipulation frequency
- **Resilient fallback** — a rule-based detection system keeps the app functional if the LLM provider is rate-limited or unavailable

## Tech Stack

**Frontend:** React, Vite
**Backend:** FastAPI, SQLAlchemy, SQLite
**AI:** Groq API (Llama 3.3)
**Deployment:** Vercel (frontend), Render (backend)

## Architecture

```
soul_lense_ai/
├── frontend/          React + Vite single-page app
│   └── src/
│       └── pages_old/ Analysis, Dashboard, History, Relationship pages
└── backend/           FastAPI application
    ├── main.py        API routes
    ├── models.py      SQLAlchemy models
    ├── database.py    DB session config
    └── services/
        └── ai_service.py  LLM integration + fallback logic
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/analyze` | Analyze a single message for emotion and manipulation |
| `GET` | `/history` | Retrieve recent analyses |
| `GET` | `/dashboard` | Aggregate stats across all analyses |
| `POST` | `/relationship` | Compare two participants in an exchange |
| `POST` | `/conversation-analysis` | Summarize and analyze a full conversation |

## Running Locally

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Create a `.env` file in `backend/` with:
```
GROQ_API_KEY=your_groq_api_key
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Author

Built by [Nazeeya Banu H](https://github.com/nazeeyabanuh)
