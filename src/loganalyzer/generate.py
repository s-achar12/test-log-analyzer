import random
from datetime import datetime, timedelta

FAILURES = [
    "TIMEOUT waiting for signal VehicleSpeed",
    "SIGNAL_MISMATCH expected=72 actual=0",
    "FLASH_ERROR block=0x3A checksum failed",
    "UNEXPECTED_DTC code=P0301",
]

def make_log(n_lines: int = 20, seed: int | None = None) -> list[str]:
    rng = random.Random(seed)
    start = datetime(2026, 1, 1, 9, 0, 0)
    lines = []
    for i in range(n_lines):
        ts = start + timedelta(seconds=i * 2)
        level = "INFO"
        msg = "step ok"
        if rng.random() < 0.2:
            level = "ERROR"
            msg = rng.choice(FAILURES)
        lines.append(f"{ts.isoformat()} [{level}] {msg}")
    return lines

if __name__ == "__main__":
    for line in make_log(10, seed=42):
        print(line)