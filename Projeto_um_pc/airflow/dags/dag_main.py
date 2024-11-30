from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Função para executar o script landing.py
def executar_script_landing():
    script_path = "/opt/airflow/dags/tasks/landing.py"  # Caminho do script no contêiner
    subprocess.run(["python", script_path], check=True)

# Definição da DAG
with DAG(
    dag_id="landing_dag",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
    },
    description="DAG para executar o script landing.py",
    schedule_interval=None,  # Para execução manual. Você pode usar cron aqui, ex: "0 12 * * *"
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    # Tarefa para executar o script
    executar_landing_task = PythonOperator(
        task_id="executar_landing_script",
        python_callable=executar_script_landing
    )

    executar_landing_task
