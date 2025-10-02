import pandas as pd
import numpy as np

def fill_na(st_dt,ed_dt,df):
    df['dttm'] = pd.to_datetime(df.dttm)
    df.sort_values(['fc_name', 'dttm'], inplace=True)

    df_copy = None
    fc_list = sorted(df.fc_name.unique())

    date_time_hour_index = pd.date_range(st_dt, ed_dt, freq='H')

    for fc_name in fc_list:
        df_ = df.query(f"fc_name=='{fc_name}'")
        df_.set_index("dttm", inplace=True)
        df_ = df_.reindex(date_time_hour_index)
        df_["fc_name"].fillna(method='ffill',inplace=True)
        df_["fc_name"].fillna(method='bfill',inplace=True)
        df_.fillna(0,inplace=True)
        df_.reset_index(inplace=True)
        df_.rename(columns={'index':'dttm'},inplace=True)
        df_["hr"] = df_.dttm.dt.hour
        if df_copy is None:
            df_copy = df_
        else:
            df_copy = pd.concat([df_copy,df_])

    return df_copy