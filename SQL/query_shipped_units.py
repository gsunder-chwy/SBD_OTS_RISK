from configs import fc_list
from utils.snowflake_pull import execute_query_and_return_formatted_data
import os
import pandas as pd


def query_shipped_units(dt_string_start: str,dt_string_end: str):
    """Queries the snowflake database for actual shipped units between start and end date.
        Writes out the results in the data folder as a csv
        Args:
            dt_string_start: start date for query
            dt_string_end: end date for query
        Returns:
            None
    """
    shipped_units_data = None
    #get the dirname in SQL
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #append the specific file path
    sql_path = os.path.join(BASE_DIR, "shipped_units.sql")
    #move one level up to save in the data folder
    BASE_DIR = os.path.dirname(BASE_DIR)
    for st, end in zip(dt_string_start[::-1], dt_string_end[::-1]):
        print(f"Reading Shipping Units data for {st}")

        with open(sql_path, "r") as file:
            shipped_units_sql = file.read()

        params = {'st': st, 'end': end, 'fc_list': fc_list}

        shipped_units_sql = shipped_units_sql.format(**params)

        shipped_units_ = execute_query_and_return_formatted_data(query=shipped_units_sql)

        if shipped_units_data is None:
            shipped_units_data = shipped_units_
        else:
            shipped_units_data = pd.concat([shipped_units_data, shipped_units_])

        print(f" Done reading PDD order-orderlines on {st} of size {shipped_units_.shape}")

    shipped_units_data.to_csv(os.path.join(BASE_DIR,"data","shipped_units_data.csv"), index=False)