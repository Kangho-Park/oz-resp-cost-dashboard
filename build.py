"""Fetch sheet tabs -> run metrics/*.py -> dist/index.html.  Usage: python build.py [--refresh]"""
import importlib.util, json, pathlib, sys, urllib.request
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "metrics"))  # lets metrics import shared helpers from metrics/_common.py
SHEET_ID = "1nPuY8AKFAs2r9da4xUBV3WMKdLEBZJGpmd3kP7xKNvU"
TABS = {"claim": 78768174, "patient": 80354650, "institution": 991582107, "sick_master": 1345263105, "code_table": 173633388, "sido_code": 2036727743, "hospital_open": 1356575315, "claim_sick": 1877573041, "claim_rx": 2056573466, "drug_ingredient": 2109510048}  # {"table_name": gid}


def fetch(refresh):
    (ROOT / "data").mkdir(exist_ok=True)
    for name, gid in TABS.items():
        f = ROOT / "data" / f"{name}.csv"
        if refresh or not f.exists():
            url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
            f.write_bytes(urllib.request.urlopen(url).read())
            print("fetched", name)
    return {n: pd.read_csv(ROOT / "data" / f"{n}.csv", dtype=str) for n in TABS}


def run_metrics(tables):
    out = []
    for p in sorted((ROOT / "metrics").rglob("*.py")):
        if p.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(p.stem, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out.append({"id": p.stem, "question": m.QUESTION, "chart": m.CHART, "data": m.run(tables)})
        print("metric", p.stem)
    return out


if __name__ == "__main__":
    metrics = run_metrics(fetch("--refresh" in sys.argv))
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    html = html.replace("/*__METRICS__*/[]", json.dumps(metrics, ensure_ascii=False))
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "index.html").write_text(html, encoding="utf-8")
    print("built dist/index.html")
