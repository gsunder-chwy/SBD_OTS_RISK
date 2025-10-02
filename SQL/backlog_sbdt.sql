with batches as(
                    select batch_id,
                           batch_dttm::timestamp as batch_dttm,
                           batchno,
                           orsitemtype
                    from orssimsdb.ors_simulations.ors2_batches
                    where batch_dttm::timestamp BETWEEN '{st}' and '{end}'
                    )
select sb.batch_id,
       sb.fc_name,
       sb.ship_by_dttm AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York' as ship_by_dttm,
       SUM(sb.units) as num_units,
       min(sb.batch_dttm AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York') as batch_dttm,
       max(b.batch_dttm) as batch_dttm_batches,
       min(sb.backlog_snapshot_dttm AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York') as backlog_snapshot_dttm
from orssimsdb.ors_simulations.ors2_athena_backlog_by_sbdt sb
join batches b
on sb.batch_id = b.batch_id
group by sb.batch_id,sb.fc_name,sb.ship_by_dttm
order by 2,5,3
;