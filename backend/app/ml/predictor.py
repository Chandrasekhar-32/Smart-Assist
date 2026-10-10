"""Internal ML module: loads the trained Scikit-learn model and predicts
the suitable learning format for a student's performance data.

If the model cannot be loaded, a rule-based fallback keeps the app reliable
during demonstrations (section 30).
"""
import os
from functools import lru_cache

from app.core.config import MODEL_PATH
from app.ml.explanation import build_reason, format_label
from app.ml.preprocessing import FEATURE_COLUMNS, FORMATS, encode_features

try:
    import joblib
except Exception:  # pragma: no cover
    joblib = None

FEATURE_NAMES = ["quiz score", "time taken", "number of attempts", "lesson difficulty",
                 "previous score", "preferred format", "progress"]


@lru_cache(maxsize=1)
def load_model():
    if joblib is None or not os.path.exists(MODEL_PATH):
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


def _top_factor(bundle, features_vec):
    """Best-effort feature importance explanation (no SHAP needed)."""
    try:
        model = bundle["format_model"]
        importances = getattr(model, "feature_importances_", None)
        if importances is None:
            return None
        idx = int(max(range(len(importances)), key=lambda i: importances[i]))
        return FEATURE_NAMES[idx]
    except Exception:
        return None


def fallback_recommendation(features: dict) -> dict:
    """Rule-based fallback used when the ML service/model is unavailable."""
    score = float(features.get("score", 0))
    attempts = int(features.get("attempts", 1))
    pref = str(features.get("preferred_format") or features.get("preferredFormat") or "TEXT").upper()

    if score < 50 or attempts >= 3:
        need = "HIGH"
        fmt = "AUDIO" if pref == "AUDIO" else "SIMPLIFIED_TEXT"
    elif score < 70 or attempts == 2:
        need = "MODERATE"
        fmt = "VISUAL"
    else:
        need = "EASY"
        fmt = pref if pref in ("TEXT", "SHORT_LESSON", "AUDIO") else "TEXT"

    reason = build_reason(features, fmt, need, source="fallback")
    return {
        "recommendedFormat": fmt,
        "recommendedFormatLabel": format_label(fmt),
        "difficulty": need,
        "confidence": 0.60,
        "reason": reason,
        "source": "fallback",
    }


def predict(features: dict) -> dict:
    """Return {recommendedFormat, difficulty, confidence, reason, source}."""
    bundle = load_model()
    if bundle is None:
        return fallback_recommendation(features)

    try:
        x = encode_features(features)
        fmt_model = bundle["format_model"]
        need_model = bundle["need_model"]
        fmt = str(fmt_model.predict(x)[0])
        need = str(need_model.predict(x)[0])
        proba = float(max(fmt_model.predict_proba(x)[0]))
        confidence = round(min(0.99, max(0.5, proba)), 2)
        top = _top_factor(bundle, x[0])
        reason = build_reason(features, fmt, need, source="ml", top_factor=top)
        return {
            "recommendedFormat": fmt,
            "recommendedFormatLabel": format_label(fmt),
            "difficulty": need,
            "confidence": confidence,
            "reason": reason,
            "source": "ml",
        }
    except Exception:
        return fallback_recommendation(features)
