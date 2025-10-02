import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def model_feature_gen(df):
    df["ds"] = pd.to_datetime(df["dttm"])

    df["diff_units"] = df.num_units.diff()
    df.dropna(axis=0, inplace=True)

    df["y"] = df["num_units"]  # df["diff_units"]

    df["fc_code"] = df["fc_name"].astype("category").cat.codes
    df["fc_type_code"] = df["fc_code"].astype("category").cat.codes

    return df

def test_train_split(train_start, train_end, test_start, test_end, df):
    train_start = datetime.strptime(train_start,  "%Y-%m-%d %H:%M:%S")
    train_end = datetime.strptime(train_end, "%Y-%m-%d %H:%M:%S")

    test_start = datetime.strptime(test_start, "%Y-%m-%d %H:%M:%S")
    test_end = datetime.strptime(test_end, "%Y-%m-%d %H:%M:%S")

    train = df[np.logical_and(df.ds >= train_start, df.ds < train_end)]

    test = df[np.logical_and(df.ds >= test_start, df.ds < test_end)]

    return train, test
