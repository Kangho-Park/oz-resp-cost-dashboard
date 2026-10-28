"""Inject the public Supabase config into template.html -> dist/index.html.  Usage: python build.py
Needs SUPABASE_URL and SUPABASE_ANON_KEY (environment or .env). The anon key is public; raw tables are closed by RLS."""
import json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent


def env(name):
    f = ROOT / ".env"
    if name not in os.environ and f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            k, _, v = line.partition("=")
            if k.strip() == name:
                return v.strip().strip('"\'')
    if name not in os.environ:
        raise SystemExit(f"{name} is not set")
    return os.environ[name]


if __name__ == "__main__":
    cfg = {"url": env("SUPABASE_URL").rstrip("/"), "key": env("SUPABASE_ANON_KEY")}
    html = (ROOT / "template.html").read_text(encoding="utf-8").replace("/*__CONFIG__*/{}", json.dumps(cfg), 1)
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "index.html").write_text(html, encoding="utf-8")
    print("built dist/index.html")
