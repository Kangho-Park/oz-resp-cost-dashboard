create or replace function m_13_sido(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('columns', jsonb_build_array('시도','건수','중앙값(원)'), 'rows', coalesce(jsonb_agg(rw order by med desc, sido_nm collate "C"), '[]'))
  from (select med, sido_nm, jsonb_build_array(sido_nm, to_char(n, 'FM999,999,999'), to_char(round(med), 'FM999,999,999')) rw
        from (select sc.sido_nm, count(*) n, percentile_cont(.5) within group (order by r.amt) med
              from resp(p_from, p_to) r join sido_code sc on sc.sido_cd = r.sido_cd group by sc.sido_nm) g) s
$$;
revoke all on function m_13_sido(text, text) from public, anon, authenticated;
insert into metric_registry values ('13_sido', 'm_13_sido', '환자 거주 시도별 건수와 중앙값 (건수가 적은 시도는 불안정)', 'table', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
