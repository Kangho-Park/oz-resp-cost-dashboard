"""Regression check: dashboard() called over REST with the anon key (same path as the browser) vs the original pandas metrics in verify/ over data/*.csv."""
import importlib.util, json, pathlib, sys, urllib.request
import pandas as pd
from build import env

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "verify"))  # the pandas metrics import _common from here
TABLES = ["claim", "patient", "institution", "sick_master", "code_table", "sido_code"]


def same(a, b):
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 0.5
    return a == b


def main():
    t = {n: pd.read_csv(ROOT / "data" / f"{n}.csv", dtype=str) for n in TABLES}
    url, key = env("SUPABASE_URL"), env("SUPABASE_ANON_KEY")
    req = urllib.request.Request(f"{url}/rest/v1/rpc/dashboard", b"{}", {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    sql = {m["id"]: m for m in json.load(urllib.request.urlopen(req))}
    bad = 0
    for p in sorted((ROOT / "verify").glob("[0-9]*.py")):
        spec = importlib.util.spec_from_file_location(p.stem, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        ok = p.stem in sql and same(m.run(t), sql[p.stem]["data"])
        bad += not ok
        print("OK  " if ok else "DIFF", p.stem)
        if not ok:
            print("  pandas:", m.run(t))
            print("  sql   :", sql.get(p.stem, {}).get("data"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
