# SmartAssist

**AI-Driven Multimodal and Personalized Adaptive Learning Platform**

SmartAssist does not just serve fixed content. It observes how a student learns
and performs, analyses the performance with a Scikit-learn model, and recommends
the learning format + difficulty that fits that student right now.

```
Learn → Quiz → Analyse (ML) → Recommend → Learn again → Quiz → Compare → New recommendation
```

## Tech stack

- **Frontend:** React 18 + React Router + Vite (HTML/CSS/JS)
- **Backend:** Python FastAPI, SQLAlchemy, Pydantic, JWT auth (single backend — no separate ML server)
- **Database:** PostgreSQL in production (`DATABASE_URL`), SQLite out of the box for the demo
- **ML:** Scikit-learn (two RandomForest classifiers) + Pandas/NumPy, trained by `app/ml/train.py`

## Project structure

```
smartassist/
├── frontend/          React SPA (components, pages, services, context, routes)
├── backend/           FastAPI app
│   ├── app/routes|services|repositories|models|schemas|ml|core|database
│   ├── app/ml/recommendation_model.pkl
│   ├── tests/test_api.py        42 end-to-end API checks
│   └── requirements.txt
├── database/          schema.sql + seed.sql (PostgreSQL)
├── docs/              architecture, API and database documentation
└── README.md
```

## Run it

Backend (port 8000):

```bash
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m app.ml.train        # optional: model trains on first start too
.venv/bin/uvicorn app.main:app --port 8000
```

Frontend (port 3000, proxies `/api` → backend):

```bash
cd frontend
npm install
npm run dev
```

First start creates the tables and seeds 3 subjects / 15 lessons / quizzes /
demo users with performance history.

## Demo accounts

| Role    | Email                   | Password   |
|---------|-------------------------|------------|
| Student | student@smartassist.edu | student123 |
| Teacher | teacher@smartassist.edu | teacher123 |

Student flow: **Dashboard → Computer Science → Binary Numbers → choose format →
Take Quiz → score + recommendation with reason → Recommended lesson → retake →
improvement detected → new recommendation.**

Teacher flow: **Dashboard → click a student → scores, attempts and the exact
explanation behind every ML recommendation.**

## Tests

```bash
cd backend
.venv/bin/python tests/test_api.py    # 42 checks: auth, RBAC, quiz, ML, teacher
```

## Key design rules

- Every recommendation includes a human-readable **reason** (explainability)
- ML model with rule-based **fallback** if the model file is unavailable
- Role-based access: students cannot call teacher APIs and vice versa
- Passwords stored only as salted PBKDF2 hashes; JWT for all protected routes
- No paid APIs, no video hosting, no extra features — the innovation is the
  **personalized adaptive recommendation system**
