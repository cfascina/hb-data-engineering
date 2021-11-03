import airflow

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id = 'dag_dates',
    default_args = args,
    schedule_interval = '@daily',
    dagrun_timeout = timedelta(minutes = 60)
)

task_01 = BashOperator(
    task_id = 'task_dates',
    bash_command = 'date',
    dag = dag
)

task_02 = BashOperator(
    task_id = 'sleep_10',
    bash_command = 'sleep 10',
    retries = 3,
    dag = dag
)

task_03 = BashOperator(
    task_id = 'output',
    bash_command = 'date > /opt/airflow/outputs/date.txt',
    retries = 3,
    dag = dag
)

task_01 >> task_02 >> task_03