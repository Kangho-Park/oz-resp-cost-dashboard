"""One metric = one file. Copy to metrics/<snake_case_id>.py (files starting with _ are skipped)."""
QUESTION = "What business question does this answer?"
CHART = "bar"  # kpi | bar | line | table


def run(t):  # t: dict of table name -> DataFrame (all columns are text; cast explicitly)
    # kpi      -> {"value": 123, "unit": "건"}
    # bar/line -> {"labels": [...], "values": [...]}
    # table    -> {"columns": [...], "rows": [[...], ...]}
    return {"labels": [], "values": []}
