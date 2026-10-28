create or replace function m_00_headline(p_from text, p_to text) returns jsonb language sql stable as $$
  with t as (select tier, percentile_cont(.5) within group (order by amt) med from resp(p_from, p_to) group by tier),
       q as (select percentile_cont(.5) within group (order by amt) med from resp(p_from, p_to) where prem_quintile is not null group by prem_quintile),
       s as (select min(med) lo, max(med) hi, percentile_cont(.5) within group (order by med) mid from q)
  select jsonb_build_object('text', case
    when (select med from t where tier = '상급종합병원') is null or (select med from t where tier = '의원') is null
    then '선택한 기간에 해당하는 데이터가 부족합니다.'
    else format('상급종합병원의 건당 중앙값은 %s원으로 의원(%s원)의 %s배입니다. 소득 5분위 간 건당 중앙값은 %s~%s원으로 %s.',
      to_char(round((select med from t where tier = '상급종합병원')), 'FM999,999,999'),
      to_char(round((select med from t where tier = '의원')), 'FM999,999,999'),
      to_char((select med from t where tier = '상급종합병원') / (select med from t where tier = '의원'), 'FM990.0'),
      to_char(round((select lo from s)), 'FM999,999,999'), to_char(round((select hi from s)), 'FM999,999,999'),
      case when ((select hi from s) - (select lo from s)) / (select mid from s) < 0.05 then '거의 같습니다' else '차이가 있습니다' end) end)
$$;
revoke all on function m_00_headline(text, text) from public, anon, authenticated;
insert into metric_registry values ('00_headline', 'm_00_headline', '한 줄 요약', 'headline', false)
  on conflict (id) do update set fn = excluded.fn, question = excluded.question, chart = excluded.chart, wide = excluded.wide;
