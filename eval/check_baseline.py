from loganalyzer.baseline import classify
from loganalyzer.generate import make_log
from loganalyzer.parse import parse_lines

df = classify(parse_lines(make_log(500, seed=99)))
print(df["category"].value_counts())