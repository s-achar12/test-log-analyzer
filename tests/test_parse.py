import pandas as pd

from loganalyzer.generate import make_log
from loganalyzer.parse import parse_lines


def test_parses_all_generated_lines():
    df = parse_lines(make_log(10, seed=42))
    assert len(df) == 10
    assert df["valid"].all()


def test_levels_are_only_info_or_error():
    df = parse_lines(make_log(50, seed=7))
    assert set(df["level"]) <= {"INFO", "ERROR"}


def test_timestamp_is_datetime():
    df = parse_lines(make_log(3, seed=1))
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])


def test_malformed_line_is_flagged():
    df = parse_lines(["this is not a log line"])
    assert not df.iloc[0]["valid"]


def test_empty_input_returns_empty_frame():
    df = parse_lines([])
    assert df.empty
    assert list(df.columns) == ["timestamp", "level", "message", "valid"]