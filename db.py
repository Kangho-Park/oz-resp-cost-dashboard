"""Shared Postgres connection: SUPABASE_DB_URL from the environment or a git-ignored .env file."""
import os, pathlib
import psycopg

ROOT = pathlib.Path(__file__).resolve().parent


def connect():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            k, _, v = line.partition("=")
            if k.strip() and not line.lstrip().startswith("#"):
                os.environ.setdefault(k.strip(), v.strip().strip('"\''))
    url = os.environ.get("SUPABASE_DB_URL")
    if not url:
        raise SystemExit("SUPABASE_DB_URL is not set (put it in .env; see .env.example)")
    return psycopg.connect(url, autocommit=False)
