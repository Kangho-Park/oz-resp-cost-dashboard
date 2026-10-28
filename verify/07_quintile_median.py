from _common import resp

QUESTION = "보험료 5분위별 중앙값 진료비 (원, 1분위가 가장 낮음)"
CHART = "bar"


def run(t):
    m = resp(t).dropna(subset=["prem_quintile"]).groupby("prem_quintile").amt.median()
    return {"labels": [f"{q}분위" for q in m.index], "values": [round(float(v)) for v in m.values]}
