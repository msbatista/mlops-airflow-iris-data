from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from scripts.experiments import random_forest_classifier
from scripts.experiments import svm_classifier
import scripts.preprocess_data as preprocess_data


DATA_DIR = '/airflow/dags/data'
DATA_URI = 'https://drive.google.com/uc?export=download&id=1rZgVuwYon_3QogTr0-v480PRpi-2l1-v'

default_args = {
    "owner": "Marcelo Batista",
    "depends_on_past": False,
    "start_date": datetime(2022, 5, 1),
    "email": "silvabatistamrcelo@gmail.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(milliseconds=5000)
}

with DAG(
        dag_id="dag_process_iris_dataset",
        schedule_interval=timedelta(minutes=10),
        catchup=False,
        default_args=default_args,
        tags=["pos", "mlops"]) as dag:

    start = EmptyOperator(task_id="start")

    with TaskGroup("pre_processing", tooltip="fetch_dataset") as pre_processing:
        t1 = BashOperator(
            dag=dag,
            task_id='download_dataset',
            bash_command="""
            cd {0}/raw
            curl -L -o iris.txt "{1}"
            """.format(DATA_DIR, DATA_URI)
        )

    with TaskGroup("etl") as etl:
        t2 = PythonOperator(
            dag=dag,
            task_id="etl",
            python_callable=preprocess_data.main
        )

    with TaskGroup("random_forest_classifier") as rfc:
        t3 = PythonOperator(
            dag=dag,
            task_id="random_forest_classifier",
            python_callable=random_forest_classifier.main
        )

    with TaskGroup("svm_classifier") as svc:
        t4 = PythonOperator(
            dag=dag,
            task_id="svm_classifier",
            python_callable=svm_classifier.main
        )

    end = EmptyOperator(task_id="end")

    start >> pre_processing >> etl >> [rfc, svc] >> end
