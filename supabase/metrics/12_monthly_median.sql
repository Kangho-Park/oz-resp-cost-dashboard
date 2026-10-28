create or replace function m_12_monthly_median(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('labels', coalesce(jsonb_agg(month order by month), '[]'), 'values', coalesce(jsonb_agg(med order by month), '[]'))
  from (select month, round(percentile_cont(.5) within group (order by amt)) med from resp(p_from, p_to) group by month) s
$$;
revoke all on function m_12_monthly_median(text, text) from public, anon, authenticated;
insert into metric_registry values ('12_monthly_median', 'm_12_monthly_median', '월별 중앙값 진료비 (원)', 'line', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
