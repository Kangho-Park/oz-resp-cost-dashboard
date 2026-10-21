from _common import resp

QUESTION = "환자 거주 시도별 건수와 중앙값 (건수가 적은 시도는 불안정)"
CHART = "table"


def run(t):
    c = resp(t).merge(t["sido_code"][["sido_cd", "sido_nm"]], on="sido_cd")
    g = c.groupby("sido_nm").amt.agg(n="size", med="median").sort_values("med", ascending=False)
    return {"columns": ["시도", "건수", "중앙값(원)"],
            "rows": [[k, f"{r.n:,}", f"{round(r.med):,}"] for k, r in g.iterrows()]}
