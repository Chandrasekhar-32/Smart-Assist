# SmartAssist API Documentation

Base URL: `/api` (the React dev server proxies `/api` and `/predict` to
`http://127.0.0.1:8000`). Interactive docs: `http://127.0.0.1:8000/docs`.

All protected endpoints require `Authorization: Bearer <JWT>`.

## Authentication

| Method | Path                  | Body | Returns |
|--------|-----------------------|------|---------|
| POST   | /api/auth/register    | name, email, password, role, age?, preferred_format? | token + user (creates student profile) |
| POST   | /api/auth/login       | email, password | token + user |

## Student

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/student/profile | profile incl. preferred format + learning requirement |
| PUT    | /api/student/profile | update name/age/preferred format |
| GET    | /api/student/dashboard | cards, continue learning, recommendation, recent performance, subject progress |
| GET    | /api/student/lessons | all lessons with progress/status |
| GET    | /api/student/progress | overall progress, average score, improvement, subject bars, recent quizzes |

## Subjects & Lessons

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/subjects | 3 subjects with lesson count + progress |
| GET    | /api/subjects/{id}/lessons | lesson cards (title, difficulty, progress, status) |
| GET    | /api/lessons/{id} | lesson detail with 5 resources, quiz id, recommendation |
| GET    | /api/lessons/{id}/resources | resources only |
| POST   | /api/lessons/{id}/view | mark lesson as opened (progress ≥ 15%) |

## Quiz & Attempts

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/quizzes/{id} | 5 questions (correct answers never sent) |
| POST   | /api/quizzes/{id}/submit | answers[] + time_taken → score, %, attempt number, performance, recommendation |
| GET    | /api/attempts | own attempt history |

## Recommendations (ML)

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/recommendations | own recommendation history with reasons |
| GET    | /api/recommendations/latest | latest recommendation |
| POST   | /api/recommendations/generate | {lesson_id?} regenerate from latest attempt |
| POST   | /api/predict (also /predict) | raw ML call: {score, timeTaken, attempts, lessonDifficulty, previousScore, preferredFormat, progress} → {recommendedFormat, difficulty, confidence, reason} |

## Teacher (TEACHER role only)

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/teacher/dashboard | totals + student performance table |
| GET    | /api/teacher/students | student rows with status (Good/Average/Needs Support) |
| GET    | /api/teacher/students/{id} | detail: scores, progress, attempts, current recommendation + reason |
| GET    | /api/teacher/students/{id}/performance | recent performance + recommendation history |
| GET    | /api/teacher/recommendations | all generated recommendations |
| GET    | /api/teacher/attempts | all quiz attempts |

## Example: POST /api/predict

Request:
```json
{"score": 42, "timeTaken": 15, "attempts": 3, "lessonDifficulty": "MEDIUM",
 "previousScore": 50, "preferredFormat": "VISUAL", "progress": 40}
```
Response:
```json
{"recommendedFormat": "SIMPLIFIED_TEXT", "recommendedFormatLabel": "Simplified Explanation",
 "difficulty": "HIGH", "confidence": 0.94,
 "reason": "Your recent performance indicates that your recent quiz score was 42%, you needed 3 attempts. ...",
 "source": "ml"}
```

Errors: 400 bad input, 401 missing/invalid token, 403 wrong role, 404 not found.
