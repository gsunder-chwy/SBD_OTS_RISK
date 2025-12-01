import sys
import json
import snowflake.connector as sf
import snowflake
import pandas as pd
import boto3

def get_secret_as_dict(
    secret_name,
    region_name = None
):
    """
    Fetches a Secrets Manager secret and returns it as a dict.
    The secret should be a JSON object (see example in the docstring above).
    """

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


def connect_snowflake_from_secret(secret):
    """
    Creates a Snowflake connection using fields from the secret dict.
    Expected keys: account, user, password, warehouse, database, schema (role optional).
    """

    conn_kwargs = dict(
        url=secret["sfUrl"],
        account="chewy.us-east-1",
        user=secret["sfUser"],
        password=secret["sfPassword"],
        warehouse=secret["sfWarehouse"],
        database=secret["sfDatabase"],
        client_session_keep_alive=True
    )
    if secret.get("role"):
        conn_kwargs["role"] = secret["role"]

    # You can add 'region' or 'host' if your Snowflake account uses non-default routing.
    # e.g., conn_kwargs['region'] = 'us-east-1'

    return snowflake.connector.connect(**conn_kwargs)

def run_query_to_dataframe(conn, sql: str) -> pd.DataFrame:
    """
    Executes a SQL statement and returns results as a pandas DataFrame.
    """
    # Use context manager to ensure cursor closes cleanly
    with conn.cursor() as cur:
        cur.execute(sql)
        # Efficiently fetch into pandas
        try:
            # Available with modern connector versions
            df = cur.fetch_pandas_all()
        except AttributeError:
            # Fallback if fetch_pandas_all is unavailable
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            df = pd.DataFrame(rows, columns=cols)
    return df

