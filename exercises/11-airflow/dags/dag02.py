import airflow

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from aws.aws import AwsAirflow


aws = AwsAirflow()

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0)
}

dag = DAG(
    dag_id = 'aws',
    default_args = args,
    schedule_interval = None,
    dagrun_timeout = timedelta(minutes = 60)
)

t1 = PythonOperator(
    task_id = 'download_data',
    python_callable = AwsAirflow.download_data(),
    dag = dag
)

t2 = PythonOperator(
    task_id = 'run',
    python_callable = AwsAirflow.run(),
    dag = dag
)

t3 = PythonOperator(
    task_id = 'send_file',
    python_callable = AwsAirflow.send_file(),
    dag = dag
)

t1.set_downstream(t2)
t2.set_downstream(t3)
