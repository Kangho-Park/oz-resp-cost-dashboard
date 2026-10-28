from _common import resp

QUESTION = "급성 감염(J00~J22) vs 만성·알레르기(J30~J99)"
CHART = "table"


def run(t):
    c = resp(t)
    rows = []
    for flag, name in ((True, "급성 감염 (J00~J22)"), (False, "만성·알레르기 (J30~J99)")):
        a = c[c.acute == flag].amt
        rows.append([name, f"{len(a):,}", f"{round(a.median()):,}"])
    return {"columns": ["질환군", "건수", "중앙값(원)"], "rows": rows}
