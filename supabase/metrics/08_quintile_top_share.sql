create or replace function m_08_quintile_top_share(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('labels', coalesce(jsonb_agg(prem_quintile || '분위' order by prem_quintile), '[]'), 'values', coalesce(jsonb_agg(v order by prem_quintile), '[]'), 'suffix', '%')
  from (select prem_quintile, round(100.0 * count(*) filter (where tier in ('상급종합병원','종합병원')) / count(*), 1) v
        from resp(p_from, p_to) where prem_quintile is not null group by prem_quintile) s
$$;
revoke all on function m_08_quintile_top_share(text, text) from public, anon, authenticated;
insert into metric_registry values ('08_quintile_top_share', 'm_08_quintile_top_share', '5분위별 상급종합·종합병원 이용 비중 (%)', 'bar', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
