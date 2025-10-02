select
                  warehouse as fc_name,
                  date as dt,
                  /* Outbound */
                  sum(case when name = 'Planned Total Show Hours OB Day Shift' then value::numeric(10,2) else 0.00 end)    as ob_planned_hours_dayshift,
                  sum(case when name = 'OB Actual Total Show Hours Day Shift' then value::numeric(10,2) else 0.00 end)     as ob_actual_hours_dayshift,
                  sum(case when name = 'Planned Total Show Hours OB Night Shift' then value::numeric(10,2) else 0.00 end)   as ob_planned_hours_nightshift,
                  sum(case when name = 'OB Actual Total Show Hours Night Shift' then value::numeric(10,2) else 0.00 end)    as ob_actual_hours_nightshift,
                  sum(case when name = 'Planned OB Day Shift Throughput' then value::numeric(10,2) else 0.00 end)       as ob_planned_tph_dayshift,
                  sum(case when name = 'Actual Throughput Day Shift' then value::numeric(10,2) else 0.00 end)         as ob_actual_tph_dayshift,
                  sum(case when name = 'Planned OB Night Shift Throughput' then value::numeric(10,2) else 0.00 end)      as ob_planned_tph_nightshift,
                  sum(case when name = 'Actual Throughput Night Shift' then value::numeric(10,2) else 0.00 end)        as ob_actual_tph_nightshift,
                  sum(case when name = 'Planned Units Shipped Day Shift' then value::numeric(10,2) else 0.00 end)       as ob_planned_units_dayshift,
                  sum(case when name = 'Actual Operations Units Shipped Day Shift' then value::numeric(10,2) else 0.00 end)  as ob_actual_units_dayshift,
                  sum(case when name = 'Planned Units Shipped Night Shift' then value::numeric(10,2) else 0.00 end)      as ob_planned_units_nightshift,
                  sum(case when name = 'Actual Operations Units Shipped Night Shift' then value::numeric(10,2) else 0.00 end) as ob_actual_units_nightshift,
                  sum(case when name = 'OB_Labor_Sharing_Hours_DayShift' then value::numeric(10, 2) else 0.00 end)       as ob_planned_labor_share_dayshift,
                  sum(case when name = 'OB_Labor_Sharing_Hours_NightShift' then value::numeric(10, 2) else 0.00 end)      as ob_planned_labor_share_nightshift,
                  sum(case when name = 'OB_Planned_MOT_DayShift_daily' then value::numeric(10, 2) else 0.00 end)        as ob_planned_mot_dayshift,
                  sum(case when name = 'OB_Planned_MOT_NightShift_daily' then value::numeric(10, 2) else 0.00 end)       as ob_planned_mot_nightshift,
                  sum(case when name = 'OB_Planned_OT_DayShift_daily' then value::numeric(10, 2) else 0.00 end)        as ob_planned_ot_dayshift,
                  sum(case when name = 'OB_Planned_OT_NightShift_daily' then value::numeric(10, 2) else 0.00 end)       as ob_planned_ot_nightshift,
                  sum(case when name = 'OB_Planned_VTO_Dayshift_daily' then value::numeric(10, 2) else 0.00 end)        as ob_planned_vto_dayshift,
                  sum(case when name = 'OB_Planned_VTO_Nightshift_daily' then value::numeric(10, 2) else 0.00 end)       as ob_planned_vto_nightshift
                from
                (
                  select
                    rcv.warehouse,
                    rcv.date,
                    rc.name,
                    rcv.value
                  from
                    laborplanning.rollup_calculations as rc
                  join
                    laborplanning.rollup_calculation_values as rcv
                  on rcv.rollup_calculation_id = rc.id
                  where
                    rc.name in (
                      'Planned Total Show Hours OB Day Shift',
                      'Planned Total Show Hours OB Night Shift',
                      'OB Actual Total Show Hours Day Shift',
                      'OB Actual Total Show Hours Night Shift',
                      'Planned OB Night Shift Throughput',
                      'Planned OB Day Shift Throughput',
                      'Actual Throughput Night Shift',
                      'Actual Throughput Day Shift',
                      'Planned Units Shipped Day Shift',
                      'Actual Operations Units Shipped Day Shift',
                      'Planned Units Shipped Night Shift',
                      'Actual Operations Units Shipped Night Shift'
                    )
                  and rc.status = 'PUBLISHED'
                  and rcv.date = '{sd}'
                  and rcv.workspace_id is null
                  and rcv.warehouse in {fc_list}
                  and rcv.replication_deleted_flag = false
                  and rc.replication_deleted_flag = false
                  union
                  select
                    dsv.warehouse,
                    dsv.date,
                    ds.name,
                    dsv.value
                  from
                    laborplanning.data_sources as ds
                  join
                    laborplanning.data_source_values as dsv
                  on dsv.data_source_id = ds.id
                  where
                    ds.name in (
                      'OB_Labor_Sharing_Hours_DayShift',
                      'OB_Labor_Sharing_Hours_NightShift',
                      'OB_Planned_MiscHrsAdjust_DayShift_daily',
                      'OB_Planned_MiscHrsAdjust_NightShift_daily',
                      'OB_Planned_MOT_DayShift_daily',
                      'OB_Planned_MOT_NightShift_daily',
                      'OB_Planned_OT_DayShift_daily',
                      'OB_Planned_OT_NightShift_daily',
                      'OB_Planned_VTO_Dayshift_daily',
                      'OB_Planned_VTO_Nightshift_daily'
                    )
                  and ds.status = 'PUBLISHED'
                  and dsv.date = '{sd}'
                  and dsv.workspace_id is null
                  and dsv.warehouse in {fc_list}
                  and dsv.replication_deleted_flag = false
                  and ds.replication_deleted_flag = false
                )
                group by 1,2
                order by 2,1
                ;