from _common import resp

QUESTION = "월별 명세서 수 (건, 진료 시작일 기준)"
CHART = "bar"


def run(t):
    s = resp(t).groupby("month").size()
    return {"labels": list(s.index), "values": [int(v) for v in s.values]}
