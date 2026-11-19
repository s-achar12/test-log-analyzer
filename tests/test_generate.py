from loganalyzer.generate import FAILURES, make_labeled_log, make_log


def test_one_label_per_line():
    rows = make_labeled_log(100, seed=5)
    assert len(rows) == 100


def test_same_seed_gives_same_output():
    assert make_labeled_log(50, seed=8) == make_labeled_log(50, seed=8)


def test_error_lines_have_failure_labels():
    for line, label in make_labeled_log(200, seed=4):
        if "[ERROR]" in line:
            assert label in FAILURES
        else:
            assert label == "NONE"


def test_make_log_matches_labeled_lines():
    assert make_log(30, seed=2) == [line for line, _ in make_labeled_log(30, seed=2)]


def test_noisy_mode_avoids_clean_keywords():
    for line, _ in make_labeled_log(300, seed=6, noisy=True):
        for keyword in FAILURES:
            assert keyword not in line