from _common import resp

QUESTION = "명세서 1건당 중앙값 진료비는?"
CHART = "kpi"


def run(t):
    return {"value": round(float(resp(t).amt.median())), "unit": "원"}
