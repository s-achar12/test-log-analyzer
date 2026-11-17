import pandas as pd

from loganalyzer.baseline import NOT_A_FAILURE, UNKNOWN, classify, classify_message
from loganalyzer.generate import make_log
from loganalyzer.parse import parse_lines


def test_each_failure_type_is_recognised():
    assert classify_message("TIMEOUT waiting for signal VehicleSpeed", "ERROR") == "TIMEOUT"
    assert classify_message("SIGNAL_MISMATCH expected=72 actual=0", "ERROR") == "SIGNAL_MISMATCH"
    assert classify_message("FLASH_ERROR block=0x3A checksum failed", "ERROR") == "FLASH_ERROR"
    assert classify_message("UNEXPECTED_DTC code=P0301", "ERROR") == "UNEXPECTED_DTC"


def test_info_lines_are_not_failures():
    assert classify_message("step ok", "INFO") == NOT_A_FAILURE


def test_unknown_error_is_labelled_unknown():
    assert classify_message("something new broke", "ERROR") == UNKNOWN


def test_classify_adds_category_column():
    df = classify(parse_lines(make_log(50, seed=3)))
    assert "category" in df.columns
    assert len(df) == 50


def test_every_error_gets_a_real_category():
    df = classify(parse_lines(make_log(200, seed=11)))
    errors = df[df["level"] == "ERROR"]
    assert (errors["category"] != NOT_A_FAILURE).all()
    assert (errors["category"] != UNKNOWN).all()