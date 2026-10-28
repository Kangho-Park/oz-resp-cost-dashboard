"""Fetch sheet tabs (cached in data/) -> replace the matching Supabase tables.  Usage: python load.py [--refresh]"""
import io, pathlib, sys, urllib.request
import pandas as pd
import db

ROOT = pathlib.Path(__file__).resolve().parent
SHEET_ID = "1nPuY8AKFAs2r9da4xUBV3WMKdLEBZJGpmd3kP7xKNvU"
TABS = {"claim": 78768174, "patient": 80354650, "institution": 991582107, "sick_master": 1345263105, "code_table": 173633388, "sido_code": 2036727743}  # {"table_name": gid}; only tabs the metrics use
PK = {"claim": ["mid"], "patient": ["jid"], "institution": ["yid"], "sick_master": ["sickcd"], "code_table": ["code_type", "code"], "sido_code": ["sido_cd"]}


def fetch(refresh):
    (ROOT / "data").mkdir(exist_ok=True)
    for name, gid in TABS.items():
        f = ROOT / "data" / f"{name}.csv"
        if refresh or not f.exists():
            url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
            f.write_bytes(urllib.request.urlopen(url).read())
            print("fetched", name)


def load():
    # one transaction: readers keep seeing the old data until every table is replaced
    with db.connect() as conn, conn.cursor() as cur:
        for name in TABS:
            df = pd.read_csv(ROOT / "data" / f"{name}.csv", dtype=str).drop_duplicates(PK[name])
            cur.execute(f"truncate {name}")
            with cur.copy(f"copy {name} ({','.join(df.columns)}) from stdin (format csv, header true)") as cp:
                cp.write(df.to_csv(index=False))
            print("loaded", name, len(df))


if __name__ == "__main__":
    fetch("--refresh" in sys.argv)
    load()
