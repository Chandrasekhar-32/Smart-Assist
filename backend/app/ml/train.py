"""Train the Scikit-learn recommendation model on a prepared dataset.

Run:  python -m app.ml.train
Produces app/ml/recommendation_model.pkl
"""
import os
import random

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from app.core.config import MODEL_PATH
from app.ml.preprocessing import FEATURE_COLUMNS, FORMATS, LEARNING_NEEDS, make_row

random.seed(42)
np.random.seed(42)


def _rule_label(row) -> tuple[str, str]:
    """Human-designed teaching rules used to label the prepared dataset.

    The model learns these patterns plus realistic noise, so at runtime it
    generalises instead of replaying a hard-coded if-statement."""
    score, attempts, diff, pref = row["score"], row["attempts"], row["lesson_difficulty"], row["preferred_format"]

    # mastered the lesson -> ease off (spec section 17: improved score -> normal format)
    if score >= 75:
        need = "EASY"
    elif score < 50 or attempts >= 3:
        need = "HIGH"
    elif score < 70 or attempts == 2 or diff == "HARD":
        need = "MODERATE"
    else:
        need = "EASY"

    if need == "HIGH":
        # struggling (spec section 14 example row 2): simpler explanation first
        fmt = "AUDIO" if pref == "AUDIO" else "SIMPLIFIED_TEXT"
    elif need == "MODERATE":
        # spec example row 3: harder lesson -> visual support
        fmt = "VISUAL" if diff == "HARD" else (pref if pref in ("VISUAL", "AUDIO") else "SHORT_LESSON")
    else:
        # performing well -> continue in the student's preferred format (example row 1)
        fmt = pref if pref in FORMATS and pref != "SIMPLIFIED_TEXT" else "TEXT"
    return fmt, need


def build_dataset(n: int = 600) -> list[dict]:
    rows = [
        # rows from the project specification (section 14)
        make_row(85, 5, 1, "EASY", 80, "TEXT", 90, "TEXT", "EASY"),
        make_row(42, 15, 3, "MEDIUM", 50, "VISUAL", 40, "SIMPLIFIED_TEXT", "HIGH"),
        make_row(55, 12, 2, "HARD", 60, "AUDIO", 50, "VISUAL", "MODERATE"),
        # the demo scenario row (section 33): 40% score, 15 min, 3 attempts
        make_row(40, 15, 3, "EASY", 50, "TEXT", 35, "SIMPLIFIED_TEXT", "HIGH"),
    ]
    for _ in range(n):
        score = int(np.clip(np.random.normal(62, 18), 0, 100))
        attempts = int(np.clip(np.random.choice([1, 2, 3, 4], p=[0.45, 0.3, 0.17, 0.08]), 1, 5))
        time_taken = int(np.clip(np.random.normal(6 + (100 - score) / 8, 3), 1, 30))
        diff = random.choice(["EASY", "MEDIUM", "HARD"])
        pref = random.choice(FORMATS)
        previous = int(np.clip(score + np.random.normal(0, 12), 0, 100))
        progress = int(np.clip(np.random.normal(score, 15), 0, 100))
        base = make_row(score, time_taken, attempts, diff, previous, pref, progress, "", "")
        fmt, need = _rule_label(base)
        if random.random() < 0.08:  # student behaviour is noisy: 8% label noise
            fmt = random.choice(FORMATS)
        base["recommended_format"] = fmt
        base["learning_need"] = need
        rows.append(base)
    return rows


def train():
    rows = build_dataset()
    X = np.array([[r[c] for c in FEATURE_COLUMNS] for r in rows])
    # lesson_difficulty / preferred_format are categorical strings in the spec
    # dataset; encode them numerically for the model input.
    diff_code = {"EASY": 0, "MEDIUM": 1, "HARD": 2}
    fmt_code = {f: i for i, f in enumerate(FORMATS)}
    for i, r in enumerate(rows):
        X[i, 3] = diff_code[r["lesson_difficulty"]]
        X[i, 5] = fmt_code[r["preferred_format"]]
    y_fmt = np.array([r["recommended_format"] for r in rows])
    y_need = np.array([r["learning_need"] for r in rows])

    metrics = {}
    Xtr, Xte, yf_tr, yf_te = train_test_split(X, y_fmt, test_size=0.25, random_state=42)
    fmt_model = RandomForestClassifier(n_estimators=120, random_state=42, max_depth=8)
    fmt_model.fit(Xtr, yf_tr)
    metrics["format_accuracy"] = float(accuracy_score(yf_te, fmt_model.predict(Xte)))

    _, Xte2, yn_tr, yn_te = train_test_split(X, y_need, test_size=0.25, random_state=42)
    need_model = RandomForestClassifier(n_estimators=120, random_state=42, max_depth=8)
    need_model.fit(X, y_need)
    metrics["need_accuracy"] = float(accuracy_score(yn_te, need_model.predict(Xte2)))

    bundle = {
        "format_model": fmt_model,
        "need_model": need_model,
        "feature_columns": FEATURE_COLUMNS,
        "formats": FORMATS,
        "learning_needs": LEARNING_NEEDS,
        "metrics": metrics,
        "n_samples": len(rows),
    }
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(bundle, MODEL_PATH)
    return bundle


if __name__ == "__main__":
    b = train()
    print(f"Trained on {b['n_samples']} rows -> {MODEL_PATH}")
    print("format accuracy:", round(b["metrics"]["format_accuracy"], 3),
          "| need accuracy:", round(b["metrics"]["need_accuracy"], 3))
