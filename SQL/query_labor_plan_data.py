from configs import fc_list
from datetime import datetime
from utils.snowflake_pull import execute_query_and_return_formatted_data
import os
import pandas as pd


def query_labor_plan_data(dt_string_start: str, dt_string_end: str, append=False):
    """Queries the snowflake database for labor plan data between start and end date.
            Writes out the results in the data folder as a csv
            Args:
                dt_string_start: start date for query
                dt_string_end: end date for query
            Returns:
                None
    """
    labor_plan_df = None
    # get the dirname in SQL
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # append the specific file path
    sql_path = os.path.join(BASE_DIR, "labor_plan.sql")
    # move one level up to save in the data folder
    BASE_DIR = os.path.dirname(BASE_DIR)

    for sd, ed in zip(dt_string_start[::-1], dt_string_end[::-1]):
        sd = datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
        sd = sd.date().strftime("%Y-%m-%d")
        print(f"Querying Labor Plan for date: {sd}")

        with open(sql_path, "r") as file:
            labor_plan_sql = file.read()

        params = {'sd': sd, 'fc_list': fc_list}

        labor_plan_sql = labor_plan_sql.format(**params)

        labor_plan = execute_query_and_return_formatted_data(query=labor_plan_sql)
        if labor_plan_df is None:
            labor_plan_df = labor_plan
        else:
            labor_plan_df = pd.concat([labor_plan_df, labor_plan])

    if append:
        labor_plan_df_ = pd.read_csv(os.path.join(BASE_DIR, "data", "labor_plan_data.csv"))
        labor_plan_df_["dt"] = [datetime.strptime(d,"%Y-%m-%d").date() for d in labor_plan_df_.dt]
        labor_plan_df = pd.concat([labor_plan_df_,labor_plan_df])

    labor_plan_df.drop_duplicates(subset=["fc_name","dt"], keep="last", inplace=True)

    labor_plan_df.to_csv(os.path.join(BASE_DIR, "data", "labor_plan_data.csv"), index=False)
