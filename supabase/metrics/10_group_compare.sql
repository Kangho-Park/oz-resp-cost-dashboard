create or replace function m_10_group_compare(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('columns', jsonb_build_array('질환군','건수','중앙값(원)'), 'rows', coalesce(jsonb_agg(rw order by o), '[]'))
  from (select case when acute then 1 else 2 end o,
          jsonb_build_array(case when acute then '급성 감염 (J00~J22)' else '만성·알레르기 (J30~J99)' end, to_char(count(*), 'FM999,999,999'),
          to_char(round(percentile_cont(.5) within group (order by amt)), 'FM999,999,999')) rw
        from resp(p_from, p_to) group by acute) s
$$;
revoke all on function m_10_group_compare(text, text) from public, anon, authenticated;
insert into metric_registry values ('10_group_compare', 'm_10_group_compare', '급성 감염(J00~J22) vs 만성·알레르기(J30~J99)', 'table', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
