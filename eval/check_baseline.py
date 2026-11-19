from pathlib import Path

import pandas as pd

from loganalyzer.baseline import classify
from loganalyzer.parse import parse_lines

DATA = Path("data/synthetic")


def evaluate(name: str) -> None:
    lines = (DATA / f"{name}.log").read_text(encoding="utf-8").splitlines()
    # keep_default_na=False stops pandas reading the label "NONE" as a missing value
    truth = pd.read_csv(DATA / f"{name}_labels.csv", keep_default_na=False)
    predicted = classify(parse_lines(lines))["category"].to_numpy()
    df = truth.assign(predicted=predicted)

    overall = (df["label"] == df["predicted"]).mean()
    failures = df[df["label"] != "NONE"]
    failure_acc = (failures["label"] == failures["predicted"]).mean()

    print(f"\n=== {name} ===")
    print(f"Overall accuracy:  {overall:.1%}")
    print(f"Failure accuracy:  {failure_acc:.1%}  ({len(failures)} failure lines)")
    print(pd.crosstab(df["label"], df["predicted"]))


if __name__ == "__main__":
    evaluate("clean")
    evaluate("noisy")