with tranlog_et as (
                select wh_id,
                   DATE_TRUNC('HOUR',CONVERT_TIMEZONE('UTC','America/New_York',end_tran_date_time::TIMESTAMP_NTZ)) as end_tran_date_time,
                   tran_qty,
                   outside_id,
                   item_number
                from aad.t_tran_log
                where tran_type = '341' and
                wh_id IN {fc_list} and
                CONVERT_TIMEZONE('UTC','America/New_York',end_tran_date_time::TIMESTAMP_NTZ) >= '{st}' AND
                CONVERT_TIMEZONE('UTC','America/New_York',end_tran_date_time::TIMESTAMP_NTZ) < '{end}'
)
select wh_id as FC_NAME,
           end_tran_date_time as dttm,
           HOUR(end_tran_date_time) as hr,
           SUM(tran_qty) as num_units,
           Count(distinct outside_id) as num_containers,
           Count(distinct item_number) as num_lineitems
from tranlog_et
group by 1,2,3
order by 2,1,3
;

