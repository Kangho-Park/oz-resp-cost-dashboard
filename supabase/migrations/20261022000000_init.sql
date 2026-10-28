-- Raw tables mirror the Google Sheet tabs. All columns are text (leading-zero codes); cast in resp().
create table claim (
  mid text primary key, jid text, yid text, insup_tp_cd text, fom_tp_cd text, main_sick text, sub_sick text,
  dgsbjt_cd text, recu_fr_dd text, recu_to_dd text, vst_ddcnt text, recu_ddcnt text, rvd_rpe_tamt_amt text,
  rvd_slf_brdn_amt text, rvd_insup_brdn_amt text, sopr_yn text, dgrslt_tp_cd text);
create table patient (jid text primary key, sex_tp_cd text, birth_yr text, sido_cd text, qlf_tp_cd text, prem_quintile text);
create table institution (yid text primary key, cl_cd text, region_cd text, shw_sbjt_cd text);
create table sick_master (sickcd text primary key, krnm text, sicknm text, wcd text, msick text, cdd text, sex text, max_age text, min_age text, wocd text);
create table code_table (code_type text, code text, code_nm text, primary key (code_type, code));
create table sido_code (sido_cd text primary key, sido_nm text, region_cd text, region_nm text);

create index claim_main_sick_idx on claim (main_sick text_pattern_ops);
create index claim_recu_fr_dd_idx on claim (recu_fr_dd);

-- Registry of dashboard metrics; each supabase/metrics/*.sql file upserts one row.
create table metric_registry (id text primary key, fn text not null, question text not null, chart text not null, wide boolean not null default false);

-- Raw data is never exposed: RLS on with no policies, no direct grants. The browser only calls dashboard().
alter table claim enable row level security;
alter table patient enable row level security;
alter table institution enable row level security;
alter table sick_master enable row level security;
alter table code_table enable row level security;
alter table sido_code enable row level security;
alter table metric_registry enable row level security;
revoke all on claim, patient, institution, sick_master, code_table, sido_code, metric_registry from anon, authenticated;

-- Shared scope: outpatient (031) claims whose main diagnosis is a J code, within a month range ('YYYY-MM', null = open).
create function resp(p_from text default null, p_to text default null)
returns table (mid text, main_sick text, amt numeric, tier text, acute boolean, month text, sido_cd text, prem_quintile text)
language sql stable security definer set search_path = public as $$
  select c.mid, c.main_sick, c.rvd_rpe_tamt_amt::numeric, ct.code_nm,
         substr(c.main_sick, 2, 2)::int <= 22, left(c.recu_fr_dd, 7), p.sido_cd, p.prem_quintile
  from claim c
  join institution i on i.yid = c.yid
  join patient p on p.jid = c.jid
  left join code_table ct on ct.code_type = '종별코드' and ct.code = i.cl_cd
  where c.main_sick like 'J%' and c.fom_tp_cd = '031'
    and (p_from is null or left(c.recu_fr_dd, 7) >= p_from)
    and (p_to is null or left(c.recu_fr_dd, 7) <= p_to)
$$;
revoke all on function resp(text, text) from public, anon, authenticated;

-- Runs every registered metric with the same filters; returns [{id, question, chart, wide, data}, ...].
create function dashboard(p_from text default null, p_to text default null)
returns jsonb language plpgsql stable security definer set search_path = public as $$
declare r metric_registry; out jsonb := '[]'::jsonb; d jsonb;
begin
  for r in select * from metric_registry order by id loop
    execute format('select %I($1, $2)', r.fn) into d using p_from, p_to;
    out := out || jsonb_build_object('id', r.id, 'question', r.question, 'chart', r.chart, 'wide', r.wide, 'data', d);
  end loop;
  return out;
end $$;
revoke all on function dashboard(text, text) from public, anon, authenticated;
grant execute on function dashboard(text, text) to anon, authenticated;
