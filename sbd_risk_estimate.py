import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#load data
shipped_units = pd.read_csv(os.path.join(BASE_DIR, "results", "predicted_shipped_units.csv"))
backlog_data = pd.read_csv(os.path.join(BASE_DIR, "data", "sbdt_backlog.csv"))

#censor negative values to zero
shipped_units["pred_shipped_units"] = np.where(shipped_units.pred_shipped_units<0,0.,shipped_units.pred_shipped_units)

#for each fc and date-hr compute the actual risk and predicted risk score

fc_name: str = "HOU1"
days_to_increment = 0

start_date: datetime = datetime.strptime("2025-11-29 06:00:00", "%Y-%m-%d %H:%M:%S")
end_date_: datetime = start_date + timedelta(days=days_to_increment)

while start_date <= end_date_:
    #query data within a day
    end_date = start_date + timedelta(days=1)
    if fc_name in ('RNO1','PHX1'):
        end_date = end_date + timedelta(hours=1)

    #query shipped units data for the FC and date range
    filtered_shipped_units = shipped_units.query(f"fc_name=='{fc_name}'").query(f"dttm >= '{start_date}' and dttm <= '{end_date}'")

    #query backlog data for the FC and date range
    filtered_backlog_data = backlog_data.query(f"fc_name=='{fc_name}'").\
        query(f"batch_dttm >= '{start_date}' and batch_dttm <'{end_date}'").\
        query(f"ship_by_dttm<='{end_date}'")

    #extarct hour from the datetime object
    filtered_backlog_data["hr"] = [datetime.strptime(dt,"%Y-%m-%d %H:%M:%S").hour for dt in filtered_backlog_data.batch_dttm]

    #get the earliest batch in each hour
    batch_filter = tuple(filtered_backlog_data.groupby("hr").agg(batch_hour_start=("batch_dttm",min)).batch_hour_start.to_list())

    #filter data for the first batch in each hour
    filtered_backlog_data = filtered_backlog_data.query(f"batch_dttm in {batch_filter}")

    #drop duplciates
    filtered_backlog_data = filtered_backlog_data.drop_duplicates(["batch_dttm","ship_by_dttm"])

    #list of unique sbdts
    unique_sbdts = filtered_backlog_data.query(f"ship_by_dttm>'{start_date}'").ship_by_dttm.unique()

    plot_data = None

    for batch_dttm in filtered_backlog_data.batch_dttm.unique():
        batch_dttm_ = datetime.strptime(batch_dttm, "%Y-%m-%d %H:%M:%S").replace(minute=0, second=0, microsecond=0)
        for sbdt in unique_sbdts:
            sbdt_ = datetime.strptime(sbdt,"%Y-%m-%d %H:%M:%S")
            actual_shipped_units = filtered_shipped_units.query(f"dttm>='{batch_dttm_}' and dttm <= '{sbdt_}'").num_units.sum()
            predicted_shipped_units = filtered_shipped_units.query(f"dttm>='{batch_dttm_}' and dttm <= '{sbdt_}'").pred_shipped_units.sum()
            backlog_sbdt = filtered_backlog_data.query(f"batch_dttm=='{batch_dttm}'").query(f"ship_by_dttm<='{sbdt_}'").num_units.sum()
            if plot_data is None:
                plot_data = pd.DataFrame({'eval_dttm':batch_dttm_,
                                          'sbdt': sbdt_,
                                          'actual_shipped_units':actual_shipped_units,
                                          'forecasted_shipped_units':predicted_shipped_units,
                                          'backlog_sbdt':backlog_sbdt,
                                          'risk_score_actual':min(100,backlog_sbdt*100/actual_shipped_units),
                                          'risk_score_predicted':min(100,backlog_sbdt*100/predicted_shipped_units),
                                        }, index=[0])
            else:
                row = pd.DataFrame({'eval_dttm':batch_dttm_,
                                          'sbdt': sbdt_,
                                          'actual_shipped_units':actual_shipped_units,
                                          'forecasted_shipped_units':predicted_shipped_units,
                                          'backlog_sbdt':backlog_sbdt,
                                          'risk_score_actual':min(100,backlog_sbdt*100/(actual_shipped_units+1e-6)),
                                          'risk_score_predicted':min(100,backlog_sbdt*100/(predicted_shipped_units+1e-6)),
                                        }, index=[0])
                plot_data = pd.concat([plot_data,row], ignore_index=True)
    '''
    for batch_dttm in filtered_backlog_data.batch_dttm.unique():
        result = []
        batch_dttm_ = datetime.strptime(batch_dttm, "%Y-%m-%d %H:%M:%S").replace(minute=0, second=0, microsecond=0)
        for sbdt in unique_sbdts:
            sbdt_ = datetime.strptime(sbdt,"%Y-%m-%d %H:%M:%S")
            actual_shipped_units = filtered_shipped_units.query(f"dttm>='{batch_dttm_}' and dttm <= '{sbdt_}'").num_units.sum()
            predicted_shipped_units = filtered_shipped_units.query(f"dttm>='{batch_dttm_}' and dttm <= '{sbdt_}'").pred_shipped_units.sum()
            backlog_sbdt = filtered_backlog_data.query(f"batch_dttm=='{batch_dttm}'").query(f"ship_by_dttm<='{sbdt_}'").num_units.sum()
            result.append(actual_shipped_units)
        plot_data.loc[batch_dttm] = result
    '''
    plot_data.to_csv(os.path.join(BASE_DIR,"results",f"risk_estimates_{fc_name}_{start_date.date()}.csv"),
                     index=False)
    start_date = start_date + timedelta(days=1)

    #print("gathered data")

    """
    color = iter(plt.cm.rainbow(np.linspace(0, 1, len(plot_data.columns))))

    for colname in plot_data.columns:
        c = next(color)
        plt.plot([datetime.strptime(i,"%Y-%m-%d %H:%M:%S") for i in plot_data.index],
             [r[0] for r in plot_data[colname]], label= f"{colname} + capacity", linestyle = "--", color=c)
        plt.plot([datetime.strptime(i,"%Y-%m-%d %H:%M:%S") for i in plot_data.index],
             [r[1] for r in plot_data[colname]], label=f"{colname} + backlog", color = c)
    plt.legend()
    plt.xlabel("Date Time")
    plt.xticks(fontsize=6)
    plt.ylabel("Cumulative Units of Backlog or Capacity")
    plt.title(f"Backlog Risk At {fc_name} FC")
    plt.savefig(f"/Users/gsunder/Downloads/{fc_name}_FC_OTS_risk.png")
    plt.show()
    """