create or replace function m_02_tier_distribution(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('columns', jsonb_build_array('종별','건수','25%','중앙값','75%','90%'), 'rows', coalesce(jsonb_agg(rw order by o), '[]'))
  from (select o, jsonb_build_array(t, to_char(count(r.amt), 'FM999,999,999'),
          coalesce(to_char(round(percentile_cont(.25) within group (order by r.amt)), 'FM999,999,999'), '-'),
          coalesce(to_char(round(percentile_cont(.5) within group (order by r.amt)), 'FM999,999,999'), '-'),
          coalesce(to_char(round(percentile_cont(.75) within group (order by r.amt)), 'FM999,999,999'), '-'),
          coalesce(to_char(round(percentile_cont(.9) within group (order by r.amt)), 'FM999,999,999'), '-')) rw
        from unnest(array['상급종합병원','종합병원','병원','의원']) with ordinality x(t, o)
        left join resp(p_from, p_to) r on r.tier = t group by t, o) s
$$;
revoke all on function m_02_tier_distribution(text, text) from public, anon, authenticated;
insert into metric_registry values ('02_tier_distribution', 'm_02_tier_distribution', '종별 진료비 분포 (원)', 'table', true)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
