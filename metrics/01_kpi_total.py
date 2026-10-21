from _common import resp

QUESTION = "분석 대상 외래 호흡기 명세서는 몇 건인가?"
CHART = "kpi"


def run(t):
    return {"value": len(resp(t)), "unit": "건"}
