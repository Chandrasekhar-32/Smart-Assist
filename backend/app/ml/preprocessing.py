"""Feature preprocessing for the SmartAssist recommendation model."""
import numpy as np

FORMATS = ["TEXT", "SIMPLIFIED_TEXT", "VISUAL", "AUDIO", "SHORT_LESSON"]
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]
LEARNING_NEEDS = ["EASY", "MODERATE", "HIGH"]  # predicted learning difficulty

FEATURE_COLUMNS = [
    "score", "time_taken", "attempts", "lesson_difficulty",
    "previous_score", "preferred_format", "progress",
]

_DIFFICULTY_CODE = {"EASY": 0, "MEDIUM": 1, "HARD": 2}
_FORMAT_CODE = {f: i for i, f in enumerate(FORMATS)}


def encode_features(features: dict) -> np.ndarray:
    """Turn a raw performance dict into the numeric vector used by the model.

    Accepts keys: score, time_taken (or timeTaken), attempts,
    lessonDifficulty/lesson_difficulty, previousScore/previous_score,
    preferredFormat/preferred_format, progress.
    """
    difficulty = str(features.get("lesson_difficulty") or features.get("lessonDifficulty") or "MEDIUM").upper()
    preferred = str(features.get("preferred_format") or features.get("preferredFormat") or "TEXT").upper()
    vector = np.array(
        [
            float(features.get("score", 0)),
            float(features.get("time_taken", features.get("timeTaken", 0))),
            float(features.get("attempts", 1)),
            _DIFFICULTY_CODE.get(difficulty, 1),
            float(features.get("previous_score", features.get("previousScore", 0))),
            _FORMAT_CODE.get(preferred, 0),
            float(features.get("progress", 0)),
        ],
        dtype=float,
    )
    return vector.reshape(1, -1)


def make_row(score, time_taken, attempts, lesson_difficulty, previous_score,
             preferred_format, progress, recommended_format, learning_need):
    return {
        "score": score,
        "time_taken": time_taken,
        "attempts": attempts,
        "lesson_difficulty": lesson_difficulty,
        "previous_score": previous_score,
        "preferred_format": preferred_format,
        "progress": progress,
        "recommended_format": recommended_format,
        "learning_need": learning_need,
    }
