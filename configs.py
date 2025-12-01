import os
from typing import List, Dict, Tuple

#connection setting for snowflake
connection_settings_snowflake: Dict = {
    'user': os.environ.get('vertica_user'),
    'password': os.environ.get('vertica_password'),
    'authenticator': 'https://chewy.okta.com',
    'account': 'chewy.us-east-1',
    'database': 'EDLDB',
    'schema': 'public',
    'warehouse': 'SC_ORDER_ROUTING_TEAM_WH',
    'role': 'SC_ORDER_ROUTING_TEAM_DEVELOPER_DEV',
    'session_parameters': {'session_timeout': '12000', }
}

#connection setting for postgres
connection_settings_postgres: Dict = {
    'host': "db-writer-dev-global-ors-simulations-db.scff.dev.chewy.com",
            # host: fll2forsdev01.chewy.local
    'port': 5432,
    'database': "orssimsdb",
    'options': '-c idle_in_transaction_session_timeout=360000000',
    # please make sure the env has these variables
    'user': os.environ.get("POSTGRES_USER"),
    'password': os.environ.get("POSTGRES_PASSWORD"),
    'keepalives': 1,
    'keepalives_idle': 30,
    'keepalives_interval': 10,
    'keepalives_count': 5,
}

#start date for train
start_date: str = "2025-07-01 06:00:00"
#end date for test
end_date: str = "2025-11-24 06:00:00"

#FCs to make predictions for
fc_list: Tuple = ('AVP1','CLT1','MCO1','MDT1','CFC1','DAY1','PHX1','AVP2','BNA1','MCI1','RNO1','HOU1')

#{fc_name: [fc_type, day_shift_start, night_shift_start, fc_shift_type]}
fc_details: Dict = {'AVP1': ['1G',6,18,"regular"],
              'AVP2': ['2G',6,18,"regular"],
              'MDT1': ['1G',6,18,"regular"],
              'BNA1': ['2G',6,18,"regular"],
              'MCI1': ['2G',6,18,"regular"],
              'CLT1': ['1G',8,20,"regular"],
              'CFC1': ['1G',6,18,"day_shift"],
              'DAY1': ['1G',8,20,"regular"],
              'HOU1': ['2G',6,18,"day_shift"],
              'MCO1': ['1G',6,18,"regular"],
              'PHX1': ['1G',9,21,"regular"],
              'RNO1': ['2G',9,21,"regular"]
             }

#start date for train
train_start_date: str = "2025-07-01 06:00:00"
#end date for train
train_end_date: str = "2025-10-31 06:00:00"
#start date for test
test_start_date: str = "2025-10-31 06:00:00"
#end date for test
test_end_date: str = "2025-12-01 06:00:00"

#append dates
append_start_date: str = "2025-11-28 06:00:00"
#end date for test
append_end_date: str = "2025-12-01 06:00:00"
