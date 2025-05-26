from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sdk import Variable
from airflow import DAG

from helpers.clean_file import clean_data

default_args = {
    'owner': 'saber',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

try:
    data_url = Variable.get("data_url")
    print(f"Data link is: {repr(data_url)}")
except Exception as e:
    print("This is an exception")
    raise


# Define or Instantiate DAG
with DAG(dag_id='exchange_rate_etl_gcp_v09',
         start_date=datetime(2025, 5, 10, 1),
         default_args=default_args,
         catchup=False) as dag:

    download_task = BashOperator(
        task_id='download_file',
        bash_command=f'curl -o /tmp/xrate.csv {data_url}',
    )

    clean_data_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,
    )

    # Define Task Dependencies
    download_task >> clean_data_task
