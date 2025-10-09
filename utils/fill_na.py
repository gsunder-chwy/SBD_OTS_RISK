import pandas as pd
import numpy as np
from datetime import datetime

def fill_na(st_dt: datetime,ed_dt: datetime,df: pd.DataFrame):
    """ Fills missing datetime in the time series shipped units data
        some hours could be missing because of no units shipped due to:
        1. seasonal events like shift change
        2. one off events like planned or unplanned downtime at an FC
            Args:
                st_dt: start date
                ed_dt: end date
                df: dataframe to impute values to
            Returns:
                DataFrame: Returns a dataframe with the imputed values
    """
    #convert to datetime
    df['dttm'] = pd.to_datetime(df.dttm)
    #order by fc_name and dttm
    df.sort_values(['fc_name', 'dttm'], inplace=True)

    df_copy = None
    fc_list = sorted(df.fc_name.unique())

    #hourly time series between start and end_dt
    date_time_hour_index = pd.date_range(st_dt, ed_dt, freq='H')

    for fc_name in fc_list:
        df_ = df.query(f"fc_name=='{fc_name}'").copy()
        df_.drop_duplicates(subset=["fc_name","dttm"], inplace=True, keep="last")
        df_.set_index("dttm", inplace=True)
        #missing hours will have NA values
        df_ = df_.reindex(date_time_hour_index)
        #fill NA for FC_Name using ffill and bfill (if the first row is missing)
        df_["fc_name"].fillna(method='ffill',inplace=True)
        df_["fc_name"].fillna(method='bfill',inplace=True)
        #0 shipped units during the missing hours
        df_.fillna(0,inplace=True)
        df_.reset_index(inplace=True)
        df_.rename(columns={'index':'dttm'},inplace=True)
        df_["hr"] = df_.dttm.dt.hour
        if df_copy is None:
            df_copy = df_
        else:
            df_copy = pd.concat([df_copy,df_])

    return df_copy