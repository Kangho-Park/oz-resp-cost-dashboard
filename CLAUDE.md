# OZ Healthcare Claims Dashboard

Static dashboard over a Google Sheet. `python build.py [--refresh]` -> `dist/index.html`.

## Layout
- `build.py` fetch tabs (cached in data/) -> run metrics -> render template. Sheet ID and tab gids are constants at the top.
- `metrics/` one metric = one file (QUESTION, CHART, run(t)); copy `_template.py`.
- `template.html` the whole page (HTML/CSS/JS). `data/`, `dist/` are generated and git-ignored.

## Rules
- Add a metric = add one file in metrics/. Nothing else.
- Read CSVs as text (dtype=str); cast explicitly (leading-zero codes).
- Grow only when needed: >10 metrics -> subfolders; multiple pages -> pages/; template >500 lines -> assets/; this file long -> docs/.

## Status / decisions
- Stage: interview done (2 rounds, 2026-10-21) -> next: metrics design
- Next: propose metric list + page layout for approval, then build one metric at a time.

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
