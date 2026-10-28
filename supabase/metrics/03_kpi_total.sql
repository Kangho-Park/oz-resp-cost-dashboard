create or replace function m_03_kpi_total(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('value', count(*), 'unit', '건') from resp(p_from, p_to)
$$;
revoke all on function m_03_kpi_total(text, text) from public, anon, authenticated;
insert into metric_registry values ('03_kpi_total', 'm_03_kpi_total', '분석 대상 외래 호흡기 명세서는 몇 건인가?', 'kpi', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
