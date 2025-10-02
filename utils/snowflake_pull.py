import pandas as pd
from configs import connection_settings
from snowflake.connector import connect

def columns_to_lower(df):
    """Converts all column names in a DataFrame to lowercase.

    Args:
        df (DataFrame): The DataFrame to convert.

    Returns:
        DataFrame: A new DataFrame with lowercase column names.
    """
    return df.rename(columns=lambda x: x.lower())


def execute_query_and_return_formatted_data(
        query_name: str = None,
        date_col: str = None,
        query_path: str = None,
        query: str = None
):
    """Executes a Snowflake query and returns the formatted data as a DataFrame. All column names are converted to
    lowercase and the date column is set as pd.datetime.

    Args:
            query_name (str, optional): The name of the SQL query file (without extension). Defaults to None, in which case the query is assumed to be provided directly in the `query` parameter.
            date_col (str, optional): The name of the column containing date data. If provided, the column is converted to datetime format. Defaults to None.
            query_path (str): The path to the directory containing the SQL query file. Set to default
            query (str, optional): The SQL query string to execute. If provided, overrides reading the query from a file. Defaults to None.

    Returns:
        DataFrame: The DataFrame containing the results of the executed query.
    """
    if query:
        query_to_execute = query
    else:
        with open(f"{query_path}{query_name}.sql", "r") as query_file:
            query_to_execute = query_file.read()
    with connect(**connection_settings) as connection:
        df = pd.read_sql(query_to_execute, connection)

    df = columns_to_lower(df)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])

    return df