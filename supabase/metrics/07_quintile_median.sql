create or replace function m_07_quintile_median(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('labels', coalesce(jsonb_agg(prem_quintile || '분위' order by prem_quintile), '[]'), 'values', coalesce(jsonb_agg(med order by prem_quintile), '[]'))
  from (select prem_quintile, round(percentile_cont(.5) within group (order by amt)) med
        from resp(p_from, p_to) where prem_quintile is not null group by prem_quintile) s
$$;
revoke all on function m_07_quintile_median(text, text) from public, anon, authenticated;
insert into metric_registry values ('07_quintile_median', 'm_07_quintile_median', '보험료 5분위별 중앙값 진료비 (원, 1분위가 가장 낮음)', 'bar', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
