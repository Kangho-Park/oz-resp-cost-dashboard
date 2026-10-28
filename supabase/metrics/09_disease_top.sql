create or replace function m_09_disease_top(p_from text, p_to text) returns jsonb language sql stable as $$
  select jsonb_build_object('columns', jsonb_build_array('코드','상병명','건수','중앙값(원)','상급종합 비중'), 'rows', coalesce(jsonb_agg(rw order by n desc, code), '[]'))
  from (select code, n, jsonb_build_array(code, coalesce((select krnm from sick_master where sickcd = code), ''), to_char(n, 'FM999,999,999'),
          to_char(round(med), 'FM999,999,999'), to_char(100.0 * top / n, 'FM990.0') || '%') rw
        from (select left(main_sick, 3) code, count(*) n, percentile_cont(.5) within group (order by amt) med,
                     count(*) filter (where tier = '상급종합병원') top
              from resp(p_from, p_to) group by 1 order by n desc, code limit 12) g) s
$$;
revoke all on function m_09_disease_top(text, text) from public, anon, authenticated;
insert into metric_registry values ('09_disease_top', 'm_09_disease_top', '상병별 건수와 진료비 (주상병 3자리 코드 상위 12개)', 'table', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
