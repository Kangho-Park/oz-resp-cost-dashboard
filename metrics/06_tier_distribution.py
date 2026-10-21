from _common import resp, TIERS

QUESTION = "종별 진료비 분포 (원)"
CHART = "table"


def run(t):
    g = resp(t).groupby("tier").amt
    rows = []
    for tier in TIERS:
        a = resp(t)[resp(t).tier == tier].amt
        rows.append([tier, f"{len(a):,}"] + [f"{round(a.quantile(q)):,}" for q in (.25, .5, .75, .9)])
    return {"columns": ["종별", "건수", "25%", "중앙값", "75%", "90%"], "rows": rows}
