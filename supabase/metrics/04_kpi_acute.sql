create or replace function m_04_kpi_acute(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('value', count(*) filter (where acute), 'unit', '건') from resp(p_from, p_to)
$$;
revoke all on function m_04_kpi_acute(text, text) from public, anon, authenticated;
insert into metric_registry values ('04_kpi_acute', 'm_04_kpi_acute', '그중 급성 감염(J00~J22)은 몇 건인가?', 'kpi', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
