import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error

def predict_and_write_out(test, model, regresor_list):
    test_write = None
    for fc_name in test.fc_name.unique():
        test_ = test.copy().query(f"fc_name == '{fc_name}'")
        X_test = test_[regresor_list[2:]]
        y_test = test_['y']

        y_pred = model.predict(X_test)

        rmse = mean_squared_error(y_test, y_pred, squared=False)
        print(f'RMSE: for FC {fc_name} {rmse:.4f}')

        mad = mean_absolute_error(y_test, y_pred)
        print(f'MAD: for FC {fc_name} {mad:.4f}')

        if test_write is None:
            test_["pred_shipped_units"] = y_pred
            test_write = test_
        else:
            test_["pred_shipped_units"] = y_pred
            test_write = pd.concat([test_write, test_])

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(BASE_DIR)
    test_write.to_csv(os.path.join(BASE_DIR,"results","predicted_shipped_units.csv"), index=False)

