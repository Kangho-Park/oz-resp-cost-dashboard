from _common import tier_median

QUESTION = "종별 중앙값 진료비 (원, 명세서 1건당)"
CHART = "bar"


def run(t):
    m = tier_median(t)
    return {"labels": list(m.index), "values": [round(float(v)) for v in m.values]}
