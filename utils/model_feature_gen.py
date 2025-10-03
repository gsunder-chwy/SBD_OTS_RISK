import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from warnings import warn

def model_feature_gen(df: pd.DataFrame):
    """ encodes categorical variables
            Args:
                df: dataframe to be feature engineered
            Returns:
                DataFrame: Returns a dataframe with the feature engineered values
    """
    #convert str to date time
    df["ds"] = pd.to_datetime(df["dttm"])
    #first diff data for stationirizing
    df["diff_units"] = df.num_units.diff()
    df.dropna(axis=0, inplace=True)

    df["y"] = df["num_units"]  # df["diff_units"]

    #encode categorical variables
    df["fc_code"] = df["fc_name"].astype("category").cat.codes
    df["fc_type_code"] = df["fc_code"].astype("category").cat.codes

    return df

def test_train_split(train_start: str, train_end: str, test_start: str, test_end: str, df: pd.DataFrame):
    """ split the data into test train datasets
                Args:
                    train_start: string date time variable to start train data
                    train_end: string date time variable to end train data
                    test_start: string date time variable to start test data
                    test_end: string date time variable to end test data
                    df: model dataframe for split
                Returns:
                    DataFrame: Returns a dataframe with the feature engineered values
    """
    train_start = datetime.strptime(train_start,  "%Y-%m-%d %H:%M:%S")
    train_end = datetime.strptime(train_end, "%Y-%m-%d %H:%M:%S")

    test_start = datetime.strptime(test_start, "%Y-%m-%d %H:%M:%S")
    test_end = datetime.strptime(test_end, "%Y-%m-%d %H:%M:%S")

    if test_start<train_end:
        warn(f"Test data start date {test_start} < train data end date {train_end}. Possible data leakage between test and train data")

    train = df[np.logical_and(df.ds >= train_start, df.ds < train_end)]

    test = df[np.logical_and(df.ds >= test_start, df.ds < test_end)]

    return train, test
