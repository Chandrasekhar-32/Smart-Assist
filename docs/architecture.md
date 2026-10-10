# SmartAssist Architecture

## Overview

SmartAssist is an adaptive learning platform: it observes how a student learns,
analyses quiz performance with a Scikit-learn model running inside the FastAPI
backend, and recommends the next suitable learning format.

```
React.js (SPA)
   │  REST / JSON + JWT
   ▼
Python FastAPI  ──►  SQLAlchemy  ──►  PostgreSQL (production) / SQLite (demo)
   │
   ▼
ML recommendation module (same Python project, no separate ML server)
   ├── preprocessing.py   feature encoding
   ├── train.py           prepares dataset + trains the model
   ├── predictor.py       loads recommendation_model.pkl, predicts, fallback
   ├── explanation.py     human-readable reason for every recommendation
   └── recommendation_model.pkl  (Random Forest ×2)
   │
   ▼
Recommendation stored in PostgreSQL  ──►  React shows it with the reason
```

## Adaptive learning loop (core feature)

1. Student learns a lesson in one of 5 formats
   (TEXT, SIMPLIFIED_TEXT, VISUAL, AUDIO, SHORT_LESSON)
2. Student takes the 5-question quiz
3. FastAPI grades it, stores the attempt (score, %, time, attempt number)
4. Recommendation service builds the performance feature vector:
   score, time_taken, attempts, lesson_difficulty, previous_score,
   preferred_format, progress
5. ML predictor returns `{recommendedFormat, difficulty, confidence, reason}`
6. Recommendation + reason are stored and shown to student *and* teacher
7. Student studies the recommended format, retakes the quiz
8. System compares performances (improvement %) and issues a new recommendation

## Backend layering

| Layer        | Responsibility                                        |
|--------------|-------------------------------------------------------|
| routes/      | REST endpoints, auth/role checks                      |
| services/    | business logic (grading, dashboards, recommendations) |
| repositories/| database queries                                      |
| models/      | SQLAlchemy tables                                     |
| schemas/     | Pydantic request/response models                      |
| ml/          | training, prediction, explanations                    |
| core/        | config + JWT/security utilities                       |
| database/    | engine + session + declarative base                   |

## Security

- Passwords: PBKDF2-HMAC-SHA256 (120k iterations, per-user salt)
- Tokens: JWT (HS256), sent as `Authorization: Bearer <token>`
- Role-based access: STUDENT and TEACHER routes are mutually protected
- Students can only read/write their own profile, attempts and recommendations

## ML model

- Two RandomForest classifiers (recommended format, learning need)
- Trained on a prepared dataset of 604 rows (spec section 14 example rows +
  generated samples labelled by teaching rules with 8% noise)
- Held-out accuracy: format ≈ 0.88, learning need ≈ 0.99
- Rule-based fallback (`fallback_recommendation`) keeps the demo reliable if
  the model file cannot be loaded (spec section 30)
