from _common import resp

QUESTION = "상병별 건수와 진료비 (주상병 3자리 코드 상위 12개)"
CHART = "table"


def run(t):
    c = resp(t).assign(code=lambda d: d.main_sick.str[:3])
    names = t["sick_master"].drop_duplicates("sickcd").set_index("sickcd").krnm
    g = c.groupby("code").agg(n=("amt", "size"), med=("amt", "median"),
                              top=("tier", lambda s: (s == "상급종합병원").mean())).sort_values("n", ascending=False).head(12)
    rows = [[k, names.get(k, ""), f"{int(r.n):,}", f"{round(r.med):,}", f"{r.top * 100:.1f}%"] for k, r in g.iterrows()]
    return {"columns": ["코드", "상병명", "건수", "중앙값(원)", "상급종합 비중"], "rows": rows}
