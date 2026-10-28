from _common import resp

QUESTION = "그중 급성 감염(J00~J22)은 몇 건인가?"
CHART = "kpi"


def run(t):
    return {"value": int(resp(t).acute.sum()), "unit": "건"}
