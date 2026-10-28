create or replace function m_01_tier_median(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('labels', coalesce(jsonb_agg(t order by o), '[]'), 'values', coalesce(jsonb_agg(v order by o), '[]'), 'suffix', '원')
  from (select t, o, coalesce(round((select percentile_cont(.5) within group (order by amt) from resp(p_from, p_to) r where r.tier = t)), 0) v
        from unnest(array['상급종합병원','종합병원','병원','의원']) with ordinality x(t, o)) s
$$;
revoke all on function m_01_tier_median(text, text) from public, anon, authenticated;
insert into metric_registry values ('01_tier_median', 'm_01_tier_median', '종별 중앙값 진료비 (원, 명세서 1건당)', 'hbar', true)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
