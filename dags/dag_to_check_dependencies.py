from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG

default_args = {
    'owner': 'saber',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def get_sklearn():
    import sklearn
    print(f"Sklearn version ====> {sklearn.__version__}")


def get_matplotlib():
    import matplotlib
    print("helllo from mat")
    print(f"matplotlib version ====> {matplotlib.__version__}")


with DAG(dag_id="dag_get_dependencies_v3",
         default_args=default_args,
         description='This Dag to check dependencies',
         start_date=datetime(2025, 5, 10, 2),
         catchup=False) as dag:
    get_sklearn = PythonOperator(task_id='get_sklearn_package',
                                 python_callable=get_sklearn)

    get_matplotlib = PythonOperator(task_id='get_matplotlib_version',
                                    python_callable=get_matplotlib)

    get_sklearn >> get_matplotlib
