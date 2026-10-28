"""Create/replace the SQL metric functions in supabase/metrics/*.sql.  Usage: python apply_metrics.py [--init]
--init also applies supabase/migrations/*.sql (scratch/local DB only; for Supabase use `supabase db push`)."""
import pathlib, sys
import db

ROOT = pathlib.Path(__file__).resolve().parent


def main(init):
    files = sorted((ROOT / "supabase" / "migrations").glob("*.sql")) if init else []
    files += sorted((ROOT / "supabase" / "metrics").glob("*.sql"))
    with db.connect() as conn, conn.cursor() as cur:
        for f in files:
            cur.execute(f.read_text(encoding="utf-8"))
            print("applied", f.name)


if __name__ == "__main__":
    main("--init" in sys.argv)
