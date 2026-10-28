from _common import resp, tier_median

QUESTION = "한 줄 요약"
CHART = "headline"
SAME_BELOW = 0.05  # quintile medians within 5% of the overall median are called "거의 같습니다"


def run(t):
    m = tier_median(t)
    q = resp(t).dropna(subset=["prem_quintile"]).groupby("prem_quintile").amt.median()
    lo, hi = round(q.min()), round(q.max())
    spread = (q.max() - q.min()) / q.median()
    income = (f"소득 5분위 간 건당 중앙값은 {lo:,}~{hi:,}원으로 거의 같습니다."
              if spread < SAME_BELOW else
              f"소득 5분위 간 건당 중앙값은 {lo:,}~{hi:,}원으로 차이가 있습니다.")
    top, base = m["상급종합병원"], m["의원"]
    return {"text": f"상급종합병원의 건당 중앙값은 {round(top):,}원으로 의원({round(base):,}원)의 {top / base:.1f}배입니다. {income}"}
