# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# OZ Healthcare Claims Dashboard

Dynamic dashboard: Google Sheet -> Supabase Postgres -> browser calls one RPC (`dashboard(p_from, p_to)`) and renders cards. Hosted as a static page on GitHub Pages.

## Commands
- `python load.py [--refresh]` replace Supabase tables from the sheet tabs (cached in `data/`; `--refresh` re-downloads). Run monthly.
- `python apply_metrics.py` (re)create the metric SQL functions after editing `supabase/metrics/*.sql`.
- `supabase db push` apply `supabase/migrations/` (schema, RLS, `resp()`, `dashboard()`). Never edit an applied migration; add a new one.
- `python verify.py` compare SQL output with the original pandas metrics in `verify/` (regression oracle, runs on `data/*.csv`).
- `python build.py` inject `SUPABASE_URL`/`SUPABASE_ANON_KEY` into `template.html` -> `dist/index.html`.
- Env: `.env` (git-ignored, see `.env.example`). `SUPABASE_DB_URL` is a secret; the anon key is public.
- Local DB testing needs Docker running; otherwise verify against the real Supabase project.

## Architecture
- `supabase/migrations/` raw tables (all text columns), RLS on with no policies, `metric_registry`, shared scope function `resp(p_from, p_to)` (outpatient 031 + main_sick J%, month range), and `dashboard()` which runs every registered metric and returns `[{id, question, chart, wide, data}]`.
- `supabase/metrics/NN_name.sql` one metric = one file: `m_NN_name(p_from, p_to) returns jsonb` + upsert into `metric_registry`. Output shapes are the chart contract used by `template.html` (kpi `{value,unit}`, bar/line/hbar `{labels,values,suffix?}`, table `{columns,rows}`, headline `{text}`). Metrics are discovered by registry, not hard-coded in the page.
- Security model: browser only holds the anon key. anon/authenticated have no table grants and no execute on `resp`/`m_*`; only `dashboard()` is executable (security definer). New functions/tables in `public` get anon grants by Supabase default, so every new function needs `revoke all ... from public, anon, authenticated`.
- `template.html` the whole page (HTML/CSS/JS); POSTs `/rest/v1/rpc/dashboard` with the month filter, no client library.
- `verify/` legacy pandas implementation of the same metrics; update it only if you want the oracle to cover a new metric.

## Rules
- Add a metric = add one SQL file in `supabase/metrics/` (copy an existing one), then `python apply_metrics.py`.
- Read CSVs as text (dtype=str); cast explicitly in SQL (leading-zero codes).
- Grow only when needed: >10 metrics -> subfolders; multiple pages -> pages/; template >500 lines -> assets/; this file long -> docs/.

## Status / decisions
- Stage: Supabase live (project hmpjutlepovgeaziomfj; schema+13 metrics applied, data loaded, verify.py 13/13 OK on 2026-10-28) -> next: GitHub repo variables + Pages deploy, then commit
- Next: set GitHub vars SUPABASE_URL/SUPABASE_ANON_KEY and deploy. Monthly `load.py` needs SUPABASE_DB_URL in .env (not set yet; initial load was done via `supabase db query` chunks). Assistant defaults, not user-confirmed: public page (anon RPC, aggregates only) and SQL-side metrics with a month-range filter.

### User context
Health-care data analyst. Question: do claim costs differ by hospital type / region / income amid reported wealth-gap concerns? Focus: infectious respiratory disease. Periodic internal reporting, updated monthly.

### Decisions (user-confirmed)
- Compare by: 종별 (claim→institution.cl_cd) and 권역·시도 (patient.sido_cd or institution.region_cd; pick one and state it).
- Income proxy: patient.prem_quintile (보험료 5분위).
- Disease scope: J00~J22 acute infections as core; J30~J99 chronic/allergic also included (show separately from core).
- Cost measure: total cost per claim (rvd_rpe_tamt_amt); report median/quantiles, not mean.
- Outpatient only (fom_tp_cd=031) for comparisons.
- Conclusion style: describe the gap and patterns (실태 제시); no causal claims; state data limits.
- Cadence: monthly refresh, internal report.

### Assistant proposals (NOT yet confirmed)
- Minimum cell size (e.g. <30 claims -> "표본 부족"); top-1% outlier shown separately; age/sex standardisation; copay/rx cost as secondary views. User did not select these.

### Data notes / caveats
- Practice data (OZ Coding SQL 3기), 2024-01~2025-12; institution has no names (anon yid, region only).
- J claims 13,285 (35%); 99.6% outpatient. Median cost by 종별: 상급종합 50,450 / 종합 29,200 / 병원 20,100 / 의원 16,600.
- Median J cost by prem_quintile is ~flat (18,100~18,500) -> income gap in cost may be absent; 종별 mix by quintile is the more likely angle.
- Only ~102 institutions have >=30 J claims; per-institution analysis is thin.
- prem_quintile null for ~3%; main_sick only (sub_sick 96% null; claim_sick has all diagnoses).
- Pending checks: whether cl_cd 종별 (01/11/21/31) maps to code_table 종별코드; region basis; 2024 vs 2025 comparability.
