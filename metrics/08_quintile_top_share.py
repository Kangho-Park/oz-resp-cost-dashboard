from _common import resp

QUESTION = "5분위별 상급종합·종합병원 이용 비중 (%)"
CHART = "bar"


def run(t):
    c = resp(t).dropna(subset=["prem_quintile"])
    s = c.tier.isin(["상급종합병원", "종합병원"]).groupby(c.prem_quintile).mean() * 100
    return {"labels": [f"{q}분위" for q in s.index], "values": [round(float(v), 1) for v in s.values], "suffix": "%"}
