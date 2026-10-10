"""Human-readable explanations for every recommendation (section 31)."""
from app.ml.preprocessing import FORMATS

FORMAT_LABELS = {
    "TEXT": "Normal Text",
    "SIMPLIFIED_TEXT": "Simplified Explanation",
    "VISUAL": "Visual Content",
    "AUDIO": "Audio Explanation",
    "SHORT_LESSON": "Short Lesson",
}


def format_label(fmt: str) -> str:
    return FORMAT_LABELS.get(fmt, fmt)


def build_reason(features: dict, recommended_format: str, learning_need: str,
                 source: str = "ml", top_factor: str | None = None) -> str:
    score = features.get("score", 0)
    attempts = features.get("attempts", 1)
    minutes = round(features.get("time_taken", 0) / 60) if features.get("time_taken", 0) > 60 else features.get("time_taken", 0)
    previous = features.get("previous_score", 0)
    time_unit = "minutes" if features.get("time_taken", 0) > 60 or features.get("time_taken", 0) >= 2 else "minutes"
    if features.get("time_taken", 0) and features.get("time_taken", 0) <= 60:
        minutes = features.get("time_taken")
        time_unit = "seconds" if features.get("time_taken") < 60 else "minutes"

    label = format_label(recommended_format)

    if learning_need == "HIGH":
        parts = [f"Your recent quiz score was {score:.0f}%"]
        if attempts > 1:
            parts.append(f"you needed {attempts} attempts")
        else:
            parts.append(f"you spent {minutes} {time_unit}")
        reason = ("Your recent performance indicates that " + ", ".join(parts) +
                  f". SmartAssist recommends {label} with easier, clearer explanations "
                  "before you attempt the quiz again.")
    elif learning_need == "MODERATE":
        reason = (f"Your score of {score:.0f}% shows understanding with some gaps"
                  + (f" after {attempts} attempts" if attempts > 1 else "") +
                  f". {label} will reinforce the topic without slowing you down.")
    else:
        reason = (f"You scored {score:.0f}% with {attempts} attempt(s), so you are doing well. "
                  f"Continue with {label} and progress to the next difficulty level.")

    if previous and score > previous:
        reason += f" Improvement detected: {previous:.0f}% -> {score:.0f}%."
    if top_factor:
        reason += f" Strongest signal: {top_factor}."
    if source == "fallback":
        reason += " (Rule-based fallback was used because the ML model was unavailable.)"
    return reason
