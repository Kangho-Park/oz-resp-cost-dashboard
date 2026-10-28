create or replace function m_05_kpi_median(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('value', coalesce(round(percentile_cont(.5) within group (order by amt)), 0), 'unit', '원') from resp(p_from, p_to)
$$;
revoke all on function m_05_kpi_median(text, text) from public, anon, authenticated;
insert into metric_registry values ('05_kpi_median', 'm_05_kpi_median', '명세서 1건당 중앙값 진료비는?', 'kpi', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
