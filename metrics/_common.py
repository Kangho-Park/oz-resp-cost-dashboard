"""Shared scope for the respiratory metrics: outpatient (031) claims whose main diagnosis is a J code."""
import pandas as pd

TIERS = ["상급종합병원", "종합병원", "병원", "의원"]
_cache = {}


def resp(t):
    if id(t) not in _cache:
        c = t["claim"]
        c = c[c.main_sick.str.startswith("J") & (c.fom_tp_cd == "031")].copy()
        c["amt"] = pd.to_numeric(c.rvd_rpe_tamt_amt)
        c = c.merge(t["institution"][["yid", "cl_cd"]], on="yid")
        c = c.merge(t["patient"][["jid", "sido_cd", "prem_quintile"]], on="jid")
        names = t["code_table"][t["code_table"].code_type == "종별코드"].set_index("code").code_nm
        c["tier"] = c.cl_cd.map(names)
        c["acute"] = c.main_sick.str[1:3].astype(int) <= 22
        c["month"] = c.recu_fr_dd.str[:7]
        _cache[id(t)] = c
    return _cache[id(t)]


def tier_median(t):
    return resp(t).groupby("tier").amt.median().reindex(TIERS)
