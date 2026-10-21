from _common import tier_median

QUESTION = "상급종합병원 중앙값은 의원의 몇 배인가?"
CHART = "kpi"


def run(t):
    m = tier_median(t)
    return {"value": round(float(m["상급종합병원"] / m["의원"]), 2), "unit": "배"}
