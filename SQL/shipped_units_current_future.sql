with cte as (
select distinct container_id,
                AGING_STATUS
from EDLDB.AAD.t_log_cycle_time_event
where fulfillment_status = 820 AND
CONVERT_TIMEZONE('UTC','America/New_York',INSERT_DATETIME::TIMESTAMP_NTZ) BETWEEN '{st}' and '{end}' AND --'2025-12-16 06:00:00' AND '2025-12-17 05:59:59'  AND
WH_ID = '{fc_name}'--'AVP1'
),
cte2 as (
select HOUR(tpc.ACTUAL_SHIP_DATE),
       CONVERT_TIMEZONE('UTC','America/New_York',tpc.ACTUAL_SHIP_DATE::TIMESTAMP_NTZ) as ACTUAL_SHIP_DATE,
       CONVERT_TIMEZONE('UTC','America/New_York',tpc.ORIGINAL_PROMISED_PULL_DATETIME::TIMESTAMP_NTZ) as ORIGINAL_PROMISED_PULL_DATETIME,
       cte.AGING_STATUS,
       TOTAL_UNITS
from EDLDB.AAD.T_PICK_CONTAINER tpc
right join cte
ON cte.container_id = tpc.container_id
)
select DATE(ACTUAL_SHIP_DATE) as ship_date,
       HOUR(ACTUAL_SHIP_DATE) as hour,
       TIME(ORIGINAL_PROMISED_PULL_DATETIME) as CPT,
       AGING_STATUS,
       SUM(TOTAL_UNITS) as num_units
from cte2
GROUP BY DATE(ACTUAL_SHIP_DATE), HOUR(ACTUAL_SHIP_DATE), TIME(ORIGINAL_PROMISED_PULL_DATETIME), AGING_STATUS
ORDER BY 1,2,3,4