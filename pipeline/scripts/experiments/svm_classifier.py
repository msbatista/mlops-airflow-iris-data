import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse
from sklearn.svm import SVC

from typing import Union, List


DATA_DIR = "/airflow/dags/data"
DATASET = "processed/cleaned.csv"
ML_FLOW_URI = "http://localhost:5003"
EXPERIMENT_NAME = "svc-iris-db-classifier-v2"

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
ENCODER = "classEncoder"
GAMMA = 'auto'

def _eval_metrics(actual, pred) -> Union[float, float, float]:
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)

    return rmse, mae, r2


def _load_data(file: str) -> pd.DataFrame:
    return pd.read_csv(file, header=0, index_col=False)


def _split_dataset(
    df: pd.DataFrame, features: List[str], encoder: str
) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    X = df[features]
    y = df[[encoder]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    return X_train, X_test, y_train, y_test


def _run_experiment(
    experiment_id: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.DataFrame,
    y_test: pd.DataFrame,
) -> None:
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.sklearn.autolog()

        svc = SVC(gamma=GAMMA)

        svc.fit(X_train, y_train.values.ravel())
        y_pred = svc.predict(X_test)

        (rmse, mae, r2) = _eval_metrics(y_test, y_pred)

        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2", r2)
        mlflow.log_metric("MAE", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                svc, "model", registered_model_name="iris_svc_model"
            )
        else:
            mlflow.sklearn.log_model(svc, "model")


def main() -> None:
    mlflow.set_tracking_uri(ML_FLOW_URI)

    experiment_id = None

    try:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    except:
        experiment_id = mlflow.get_experiment_by_name(EXPERIMENT_NAME).experiment_id
        print(experiment_id)

    print("experiment_id: %s" % experiment_id)

    iris_df = _load_data(os.path.join(DATA_DIR, DATASET))

    X_train, X_test, y_train, y_test = _split_dataset(
        df=iris_df, features=FEATURES, encoder=ENCODER
    )

    _run_experiment(experiment_id, X_train, X_test, y_train, y_test)
