import pandas as pd

# Ordered rules: first match wins. Keep the most specific patterns first.
RULES = [
    ("TIMEOUT", "TIMEOUT"),
    ("SIGNAL_MISMATCH", "SIGNAL_MISMATCH"),
    ("FLASH_ERROR", "FLASH_ERROR"),
    ("UNEXPECTED_DTC", "UNEXPECTED_DTC"),
]

UNKNOWN = "UNKNOWN"
NOT_A_FAILURE = "NONE"


def classify_message(message: str | None, level: str | None) -> str:
    """Return a failure category for one log message."""
    if level != "ERROR" or message is None:
        return NOT_A_FAILURE
    for keyword, category in RULES:
        if keyword in message:
            return category
    return UNKNOWN


def classify(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'category' column to a parsed log DataFrame."""
    out = df.copy()
    out["category"] = [
        classify_message(m, lvl) for m, lvl in zip(out["message"], out["level"])
    ]
    return out