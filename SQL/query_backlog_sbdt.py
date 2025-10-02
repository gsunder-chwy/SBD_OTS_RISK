from configs import connection_settings_postgres
import os
import pandas as pd
import psycopg2


def query_backlog_sbdt(dt_string_start, dt_string_end):
    sbdt_backlog = None
    # get the dirname in SQL
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # append the specific file path
    sql_path = os.path.join(BASE_DIR, "backlog_sbdt.sql")
    # move one level up to save in the data folder
    BASE_DIR = os.path.dirname(BASE_DIR)

    for st, end in zip(dt_string_start[::-1], dt_string_end[::-1]):
        print(f"Querying Backlog for date {st}")

        with open(sql_path, "r") as file:
            backlog_sbdt_sql = file.read()

        params = {'st': st, 'end': end }

        backlog_sbdt_sql = backlog_sbdt_sql.format(**params)

        conn = psycopg2.connect(
            host=connection_settings_postgres['host'],
            database=connection_settings_postgres['database'],
            user=connection_settings_postgres['user'],
            password=connection_settings_postgres['password'],
            port=connection_settings_postgres['port']
        )
        cursor = conn.cursor()
        cursor.execute(backlog_sbdt_sql)

        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        sbdt_backlog_ = pd.DataFrame(rows, columns=column_names)

        if sbdt_backlog is None:
            sbdt_backlog = sbdt_backlog_
        else:
            sbdt_backlog = pd.concat([sbdt_backlog, sbdt_backlog_])

    sbdt_backlog.to_csv(os.path.join(BASE_DIR, "data", "sbdt_backlog.csv"), index=False)