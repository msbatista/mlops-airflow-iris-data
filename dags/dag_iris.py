from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
import scripts.preprocess_data as preprocess_data


DATA_DIR = '../data'

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

    with TaskGroup("etl", tooltip="fetch_dataset") as etl:
        t1 = BashOperator(
            dag=dag,
            task_id='download_dataset',
            bash_command="""
            cd {0}/raw
            curl -L -o iris.txt "https://drive.google.com/uc?export=download&id=1rZgVuwYon_3QogTr0-v480PRpi-2l1-v"
            """.format(DATA_DIR)
        )

        [t1]

        with TaskGroup("preprocess") as pre_process:
            t2 = PythonOperator(
                dag=dag,
                task_id="pre_process_etl",
                python_callable=preprocess_data.main
            )

            [t2]

    end = EmptyOperator(task_id="end")
    start >> etl >> pre_process >> end
