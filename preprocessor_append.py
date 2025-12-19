from configs import append_start_date, append_end_date, start_date, end_date
from datetime import datetime, timedelta
import os
import pandas as pd
import shutil
from SQL.query_shipped_units import query_shipped_units
from SQL.query_labor_plan_data import query_labor_plan_data
from SQL.query_backlog_sbdt import query_backlog_sbdt
from utils.fill_na import fill_na
from utils.feature_engineering import feature_engineering
from typing import List, Dict, Tuple

folder_path: str = "data"

append_start_date: datetime = datetime.strptime(append_start_date,"%Y-%m-%d %H:%M:%S")
append_end_date: datetime = datetime.strptime(append_end_date,"%Y-%m-%d %H:%M:%S")

start_date: datetime = min(datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S"), append_end_date)
end_date: datetime = max(datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S"), append_end_date)

dt_string_start: List[str] = [d.strftime("%Y-%m-%d %H:%M:%S") for d in pd.date_range(append_start_date,end_date,freq='D')]
dt_string_end: List[str] = [d.strftime("%Y-%m-%d %H:%M:%S") for d in pd.date_range(append_start_date + timedelta(days=1),
                                                                        append_end_date + timedelta(days=1),
                                                                        freq='D')]

#querry and writeout shipped units data
query_shipped_units(dt_string_start, dt_string_end, append=True)

#read fc_labor info
query_labor_plan_data(dt_string_start, dt_string_end, append=True)

#data cleaning
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
shipped_units_data: pd.DataFrame = pd.read_csv(os.path.join(BASE_DIR, "data", "shipped_units_data.csv"))
labor_plan_data: pd.DataFrame = pd.read_csv(os.path.join(BASE_DIR, "data", "labor_plan_data.csv"))

#missing hours in the data get 0 values
shipped_units_data = fill_na(start_date, end_date, shipped_units_data)

#feature engineering
feature_engineering(shipped_units_data, labor_plan_data)

# query backlog_sbdt info
#query_backlog_sbdt(dt_string_start, dt_string_end)
