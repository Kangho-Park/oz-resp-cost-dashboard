from _common import resp

QUESTION = "월별 중앙값 진료비 (원)"
CHART = "line"


def run(t):
    s = resp(t).groupby("month").amt.median()
    return {"labels": list(s.index), "values": [round(float(v)) for v in s.values]}
