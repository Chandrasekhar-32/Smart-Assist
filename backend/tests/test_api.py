"""End-to-end API smoke test for SmartAssist (run: .venv/bin/python tests/test_api.py)."""
import sys
import time
import uuid

import httpx

BASE = "http://127.0.0.1:8000"
c = httpx.Client(base_url=BASE, timeout=20)
passed, failed = [], []


def check(name, cond, detail=""):
    (passed if cond else failed).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f"  {detail}" if detail else ""))


# 1. auth
r = c.post("/api/auth/login", json={"email": "student@smartassist.edu", "password": "student123"})
check("student login", r.status_code == 200, str(r.status_code))
st = r.json()
check("jwt issued", len(st.get("access_token", "")) > 20)
S = {"Authorization": f"Bearer {st['access_token']}"}

EMAIL = f"test.{uuid.uuid4().hex[:8]}@test.com"
r = c.post("/api/auth/register", json={"name": "Test User", "email": EMAIL,
                                       "password": "secret123", "role": "STUDENT",
                                       "age": 20, "preferred_format": "VISUAL"})
check("register new student", r.status_code == 200, str(r.status_code))
r = c.post("/api/auth/register", json={"name": "Dup", "email": EMAIL, "password": "secret123"})
check("duplicate email rejected", r.status_code == 400, str(r.status_code))
r = c.post("/api/auth/login", json={"email": "student@smartassist.edu", "password": "wrong"})
check("bad password rejected", r.status_code == 401, str(r.status_code))
r = c.get("/api/student/dashboard")
check("unauthenticated blocked", r.status_code == 401, str(r.status_code))

# 2. profile + dashboard
r = c.get("/api/student/profile", headers=S)
check("get profile", r.status_code == 200 and r.json()["name"] == "Chandrasekhar")
r = c.put("/api/student/profile", headers=S, json={"age": 22, "preferred_format": "SIMPLIFIED_TEXT"})
check("update profile", r.status_code == 200 and r.json()["age"] == 22)
r = c.get("/api/student/dashboard", headers=S)
dash = r.json()
check("dashboard", r.status_code == 200, f"avg={dash['average_score']} progress={dash['progress']} "
      f"completed={dash['lessons_completed']}/{dash['total_lessons']} attempts={dash['quiz_attempts']} "
      f"improvement={dash['improvement']}")
check("dashboard has recommendation", dash.get("recommendation") is not None,
      str((dash.get("recommendation") or {}).get("recommended_format_label")))
check("dashboard recent performance", len(dash["recent_performance"]) > 0)
check("dashboard subject progress", len(dash["subject_progress"]) == 3, str(dash["subject_progress"]))

# 3. subjects + lessons
r = c.get("/api/subjects", headers=S)
subs = r.json()
check("3 subjects", len(subs) == 3, str([s["name"] for s in subs]))
r = c.get(f"/api/subjects/{subs[2]['id']}/lessons", headers=S)
lessons = r.json()
check("5 lessons per subject", len(lessons) == 5, str(len(lessons)))
check("lesson cards have progress/status", all("status" in l for l in lessons))

# 4. lesson detail + resources
r = c.get(f"/api/lessons/{lessons[0]['id']}", headers=S)
detail = r.json()
check("lesson detail", r.status_code == 200, detail["title"])
check("5 learning formats", len(detail["resources"]) == 5,
      str([x["type"] for x in detail["resources"]]))
c.post(f"/api/lessons/{lessons[0]['id']}/view", headers=S)

# 5. quiz flow
r = c.get(f"/api/quizzes/{detail['quiz_id']}", headers=S)
quiz = r.json()
check("quiz has 5 questions", len(quiz["questions"]) == 5, str(len(quiz)))
check("correct answers hidden", "correct_answer" not in quiz["questions"][0])

answers = []
for i, q in enumerate(quiz["questions"]):
    answers.append({"question_id": q["id"], "answer": "A" if i % 2 == 0 else "B"})
r = c.post(f"/api/quizzes/{detail['quiz_id']}/submit", headers=S,
           json={"answers": answers, "time_taken": 900})
res = r.json()
check("quiz submit", r.status_code == 200, "" if r.status_code == 200 else f"{r.status_code} {r.text[:200]}")
check("score/percentage computed", res.get("total") == 5 and 0 <= res.get("percentage", -1) <= 100,
      f"{res.get('score')}/{res.get('total')} = {res.get('percentage')}%")
check("time stored", res.get("time_taken") == 900)
check("attempt number", res.get("attempt_number", 0) >= 1)
check("ML recommendation returned", res.get("recommendation") is not None,
      str((res.get("recommendation") or {}).get("recommended_format_label")) +
      f" conf={(res.get('recommendation') or {}).get('confidence')} src={(res.get('recommendation') or {}).get('source')}")
check("recommendation has reason", bool((res.get("recommendation") or {}).get("reason")))

# 6. recommendations + progress + attempts
r = c.get("/api/recommendations", headers=S)
check("list recommendations", r.status_code == 200 and len(r.json()) > 0, str(len(r.json())))
r = c.get("/api/student/progress", headers=S)
prog = r.json()
check("progress page data", r.status_code == 200 and "overall_progress" in prog,
      f"overall={prog['overall_progress']} avg={prog['average_score']} attempts={prog['quiz_attempts']}")
r = c.get("/api/attempts", headers=S)
check("attempt history", r.status_code == 200 and len(r.json()) > 0, str(len(r.json())))
r = c.post("/api/recommendations/generate", headers=S, json={})
check("generate recommendation endpoint", r.status_code == 200, str(r.status_code))

# 7. direct ML endpoint (spec section 15)
r = c.post("/api/predict", headers=S, json={"score": 42, "timeTaken": 15, "attempts": 3,
                                            "lessonDifficulty": "MEDIUM", "previousScore": 50,
                                            "preferredFormat": "VISUAL", "progress": 40})
p = r.json()
check("POST /api/predict", r.status_code == 200, str(p))
check("predict matches spec example", p.get("recommendedFormat") == "SIMPLIFIED_TEXT",
      f"{p.get('recommendedFormat')} difficulty={p.get('difficulty')} conf={p.get('confidence')}")
r = c.post("/predict", headers=S, json={"score": 42, "timeTaken": 15, "attempts": 3,
                                        "lessonDifficulty": "MEDIUM", "previousScore": 50,
                                        "preferredFormat": "VISUAL", "progress": 40})
check("POST /predict alias", r.status_code == 200)

# 8. teacher flows
r = c.post("/api/auth/login", json={"email": "teacher@smartassist.edu", "password": "teacher123"})
check("teacher login", r.status_code == 200)
T = {"Authorization": f"Bearer {r.json()['access_token']}"}
r = c.get("/api/teacher/dashboard", headers=T)
td = r.json()
check("teacher dashboard", r.status_code == 200,
      f"students={td['total_students']} avg={td['average_score']} "
      f"support={td['needing_support']} recs={td['recommendations_generated']}")
check("students listed with status", len(td["students"]) >= 4 and all("status" in s for s in td["students"]) and any(s["status"] == "Good" for s in td["students"]) and any(s["status"] == "Needs Support" for s in td["students"]),
      str([(s["name"], s["avg_score"], s["status"]) for s in td["students"]]))
sid = td["students"][0]["id"]
r = c.get(f"/api/teacher/students/{sid}", headers=T)
sd = r.json()
check("teacher student details", r.status_code == 200 and "recent_performance" in sd)
check("explainable recommendation for teacher", bool((sd.get("current_recommendation") or {}).get("reason")),
      str((sd.get("current_recommendation") or {}).get("recommended_format_label")))
r = c.get(f"/api/teacher/students/{sid}/performance", headers=T)
check("student performance endpoint", r.status_code == 200)
r = c.get("/api/teacher/recommendations", headers=T)
check("teacher sees recommendations", r.status_code == 200 and len(r.json()) > 0, str(len(r.json())))
r = c.get("/api/teacher/attempts", headers=T)
check("teacher attempts", r.status_code == 200 and len(r.json()) > 0)

# 9. role isolation
r = c.get("/api/teacher/students", headers=S)
check("student blocked from teacher API", r.status_code == 403, str(r.status_code))
r2 = c.get("/api/student/dashboard", headers=T)
check("teacher blocked from student API", r2.status_code == 403, str(r2.status_code))

print(f"\n{len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
