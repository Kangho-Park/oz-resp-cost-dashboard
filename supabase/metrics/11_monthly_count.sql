create or replace function m_11_monthly_count(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('labels', coalesce(jsonb_agg(month order by month), '[]'), 'values', coalesce(jsonb_agg(n order by month), '[]'))
  from (select month, count(*) n from resp(p_from, p_to) group by month) s
$$;
revoke all on function m_11_monthly_count(text, text) from public, anon, authenticated;
insert into metric_registry values ('11_monthly_count', 'm_11_monthly_count', '월별 명세서 수 (건, 진료 시작일 기준)', 'bar', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
