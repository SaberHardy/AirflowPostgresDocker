from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow import DAG

from helpers.clean_file import clean_data

default_args = {
    'owner': 'saber',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# Define or Instantiate DAG
with DAG(dag_id='exchange_rate_etl_gcp_v06',
         start_date=datetime(2025, 5, 10, 1),
         default_args=default_args,
         catchup=False) as dag:

    download_task = BashOperator(
        task_id='download_file',
        bash_command='curl -o /tmp/xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata',
    )

    clean_data_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,
    )

    # Define Task Dependencies
    download_task >> clean_data_task
