from configs import test_start_date, test_end_date
from configs import train_start_date, train_end_date
import pandas as pd
import xgboost as xgb
from utils.model_feature_gen import test_train_split, model_feature_gen
from utils.predict import predict_and_write_out
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#read the feature engineered data
model_data = pd.read_csv(os.path.join(BASE_DIR, "data", "model_data.csv"))

#encode categorical columns
model_data = model_feature_gen(model_data)

regresor_list = ['y', 'ds', 'hr',
                 'shift_start', 'shift_start_prev_hr', 'shift_start_foll_hr', 'weekday',
                 'planned_mot_shift', 'planned_ot_shift', 'planned_vto_shift',
                 'planned_units_shift',
                 'planned_tph_shift', 'planned_hours_shift',
                 'fc_code','fc_type_code', 'day_shift_start', 'night_shift_start',
                 'planned_units_shift_mean','planned_hours_shift_mean',
                 'day_shift_flag_hr', 'night_shift_flag_hr'
                 ]

#model_data = model_data.query("fc_name=='RNO1'")

train,test = test_train_split(train_start_date, train_end_date, test_start_date, test_end_date, model_data)

X_train = train[regresor_list[2:]]
y_train = train['y']
#'reg:squarederror' 'reg:absoluteerror' reg:pseudohubererror 'count:poisson'
model = xgb.XGBRegressor(objective='reg:absoluteerror', n_estimators=1000, max_depth=100, learning_rate=0.1,
                         subsample=0.5, min_child_weight = 50,
                         alpha=1, colsample_bytree=0.9, grow_policy='lossguide')
model.fit(X_train, y_train)
print(pd.DataFrame({'regressor':regresor_list[2:],'importance':model.feature_importances_}))

#write out model predictions
folder_path = "results"

# If folder exists → delete it
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)

# Create a new folder
os.makedirs(folder_path)

predict_and_write_out(test, model, regresor_list)


