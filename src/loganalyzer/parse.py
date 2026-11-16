import re

import pandas as pd

# Matches lines like: 2026-01-01T09:00:00 [ERROR] TIMEOUT waiting for signal VehicleSpeed
LINE_RE = re.compile(r"^(?P<timestamp>\S+) \[(?P<level>\w+)\] (?P<message>.*)$")

COLUMNS = ["timestamp", "level", "message", "valid"]


def parse_lines(lines: list[str]) -> pd.DataFrame:
    """Turn raw log lines into a DataFrame. Malformed lines are kept and flagged."""
    rows = []
    for line in lines:
        match = LINE_RE.match(line.strip())
        if match is None:
            rows.append({"timestamp": None, "level": None, "message": line, "valid": False})
        else:
            rows.append({**match.groupdict(), "valid": True})

    df = pd.DataFrame(rows, columns=COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df