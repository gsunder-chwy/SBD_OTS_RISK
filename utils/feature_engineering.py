import pandas as pd
import numpy as np
from configs import fc_list, fc_details
from datetime import datetime, timedelta
import os
from typing import Dict

def add_day_of_week(labor_plan_df: pd.DataFrame):
    """day of the week feature
            Args:
                labor_plan_df: DataFrame with labor plan
            Returns:
                DataFrame: data frame with weekday column added
    """
    # add day of the week
    labor_plan_df["dt"] = [datetime.strptime(d,"%Y-%m-%d").date() for d in labor_plan_df.dt]
    labor_plan_df.sort_values(["fc_name", "dt"], inplace=True)
    labor_plan_df["weekday"] = [d.weekday() for d in labor_plan_df.dt]
    return labor_plan_df

def fc_feature_gen(labor_plan_df: pd.DataFrame, shipped_units_data: pd.DataFrame, fc_details: Dict):
    """data engineering method
                Args:
                    labor_plan_df: DataFrame with labor plan
                    shipped_units_data: DataFrame with shipped units data
                    fc_details: Dictionary with details on the FC
                Returns:
                    DataFrame: modified labor_plan and shipped units datafram
    """
    # fc_type
    labor_plan_df["fc_type"] = [fc_details[fc_name][0] for fc_name in labor_plan_df.fc_name]

    #day_shift_start
    labor_plan_df["day_shift_start"] = [fc_details[fc_name][1] for fc_name in labor_plan_df.fc_name]

    #night_shift_start
    labor_plan_df["night_shift_start"] = [fc_details[fc_name][2] for fc_name in labor_plan_df.fc_name]

    #day_shift
    labor_plan_df["day_shift_flag_fc"] = [1 if fc_details[fc_name][3]=='day_shift' else 0 for fc_name in labor_plan_df.fc_name]

    shipped_units_data["dt"] = [dt.date() if dt.hour>=6 else (dt - timedelta(days=1)).date() for dt in shipped_units_data.dttm]
    shipped_units_data = shipped_units_data.merge(labor_plan_df, on = ["fc_name","dt"])

    #if hour is >=day_shift_start and <night_shift_start then day_shift_labor
    day_shift_flag_hr = np.where(np.logical_and(shipped_units_data.hr>=shipped_units_data.day_shift_start,
                                             shipped_units_data.hr<shipped_units_data.night_shift_start),
                              1, 0)
    #if not day_shit hour and fc is not dayshift only
    night_shift_flag_hr = np.where(np.logical_and(day_shift_flag_hr==0,shipped_units_data.day_shift_flag_fc==0),1,0)

    #an hour in the day is either day or night shift
    shipped_units_data["planned_units_shift"] = shipped_units_data.ob_planned_units_dayshift*day_shift_flag_hr + \
                                   shipped_units_data.ob_planned_units_nightshift * night_shift_flag_hr

    shipped_units_data["planned_hours_shift"] = shipped_units_data.ob_planned_hours_dayshift * day_shift_flag_hr + \
                                         shipped_units_data.ob_planned_hours_nightshift * night_shift_flag_hr

    shipped_units_data["planned_tph_shift"] = shipped_units_data.ob_planned_tph_dayshift * day_shift_flag_hr + \
                                         shipped_units_data.ob_planned_tph_nightshift * night_shift_flag_hr

    shipped_units_data["planned_laborshare_shift"] = shipped_units_data.ob_planned_labor_share_dayshift * day_shift_flag_hr + \
                                         shipped_units_data.ob_planned_labor_share_nightshift * night_shift_flag_hr

    shipped_units_data["planned_mot_shift"] = shipped_units_data.ob_planned_mot_dayshift * day_shift_flag_hr + \
                                               shipped_units_data.ob_planned_mot_nightshift * night_shift_flag_hr

    shipped_units_data["planned_ot_shift"] = shipped_units_data.ob_planned_ot_dayshift * day_shift_flag_hr + \
                                       shipped_units_data.ob_planned_ot_nightshift * night_shift_flag_hr

    shipped_units_data["planned_vto_shift"] = shipped_units_data.ob_planned_vto_dayshift * day_shift_flag_hr + \
                                       shipped_units_data.ob_planned_vto_nightshift * night_shift_flag_hr
    #flag for shift start
    shipped_units_data["shift_start"] = np.where(np.logical_or(shipped_units_data.hr == shipped_units_data.day_shift_start,
                                                        shipped_units_data.hr == shipped_units_data.night_shift_start),1,0)
    #flag for the hour prior to shift start
    shipped_units_data["shift_start_prev_hr"] = np.where(np.logical_or(shipped_units_data.hr+1 == shipped_units_data.day_shift_start,
                                                        shipped_units_data.hr+1 == shipped_units_data.night_shift_start),1,0)
    #flag for hour following shift start
    shipped_units_data["shift_start_foll_hr"] = np.where(np.logical_or(shipped_units_data.hr - 1 == shipped_units_data.day_shift_start,
                                                  shipped_units_data.hr - 1 == shipped_units_data.night_shift_start),1,0)

    return shipped_units_data, labor_plan_df

def feature_engineering(shipped_units_data: pd.DataFrame, labor_plan_df: pd.DataFrame):
    """data engineering method wrapper function, writes out the feature engineered data in the data folder
                    Args:
                        labor_plan_df: DataFrame with labor plan
                        shipped_units_data: DataFrame with shipped units data
                    Returns:
                        None
    """
    labor_plan_df = add_day_of_week(labor_plan_df)

    shipped_units_data, labor_plan_df = fc_feature_gen(labor_plan_df, shipped_units_data, fc_details)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    shipped_units_data.to_csv(os.path.join(BASE_DIR, "../data", "model_data.csv"), index= False)