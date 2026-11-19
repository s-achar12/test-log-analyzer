import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Clean mode: failure messages always contain the category keyword.
FAILURES = {
    "TIMEOUT": ["TIMEOUT waiting for signal VehicleSpeed"],
    "SIGNAL_MISMATCH": ["SIGNAL_MISMATCH expected=72 actual=0"],
    "FLASH_ERROR": ["FLASH_ERROR block=0x3A checksum failed"],
    "UNEXPECTED_DTC": ["UNEXPECTED_DTC code=P0301"],
}

# Noisy mode: same failures, worded the way real logs vary.
NOISY_FAILURES = {
    "TIMEOUT": [
        "no response from ECU within 5000 ms",
        "Timed out waiting for VehicleSpeed update",
    ],
    "SIGNAL_MISMATCH": [
        "VehicleSpeed value 0 differs from expected 72",
        "signal check failed: got 0, wanted 72",
    ],
    "FLASH_ERROR": [
        "download aborted: checksum mismatch in block 0x3A",
        "flashing failed at block 0x3A",
    ],
    "UNEXPECTED_DTC": [
        "fault code P0301 present after ignition cycle",
        "diagnostic trouble code P0301 logged unexpectedly",
    ],
}


def make_labeled_log(
    n_lines: int = 20, seed: int | None = None, noisy: bool = False
) -> list[tuple[str, str]]:
    """Return (log_line, true_label) pairs. Label is NONE for normal lines."""
    rng = random.Random(seed)
    pool = NOISY_FAILURES if noisy else FAILURES
    start = datetime(2026, 1, 1, 9, 0, 0)
    rows = []
    for i in range(n_lines):
        ts = start + timedelta(seconds=i * 2)
        if rng.random() < 0.2:
            label = rng.choice(list(pool))
            msg = rng.choice(pool[label])
            level = "ERROR"
        else:
            label, msg, level = "NONE", "step ok", "INFO"
        rows.append((f"{ts.isoformat()} [{level}] {msg}", label))
    return rows


def make_log(n_lines: int = 20, seed: int | None = None, noisy: bool = False) -> list[str]:
    """Log lines only (kept so earlier code and tests keep working)."""
    return [line for line, _ in make_labeled_log(n_lines, seed, noisy)]


def write_dataset(
    out_dir: str | Path, name: str, n_lines: int, seed: int, noisy: bool = False
) -> None:
    """Write <name>.log and <name>_labels.csv; row i of the CSV labels line i."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = make_labeled_log(n_lines, seed, noisy)

    log_text = "\n".join(line for line, _ in rows) + "\n"
    (out_dir / f"{name}.log").write_text(log_text, encoding="utf-8")

    with open(out_dir / f"{name}_labels.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line_no", "label"])
        for i, (_, label) in enumerate(rows):
            writer.writerow([i, label])


if __name__ == "__main__":
    out = Path("data/synthetic")
    write_dataset(out, "clean", 500, seed=1, noisy=False)
    write_dataset(out, "noisy", 500, seed=2, noisy=True)
    print(f"Wrote datasets to {out}/")
    for line in make_log(5, seed=1):
        print(line)