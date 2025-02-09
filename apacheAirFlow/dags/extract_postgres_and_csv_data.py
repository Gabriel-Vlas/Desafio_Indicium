from airflow import DAG
from airflow.operators.bash import BashOperator  # Importação correta para BashOperator
from airflow.operators.python import PythonOperator  # Para o PythonOperator
from datetime import datetime
import subprocess

# Caminho dos scripts
meltano_script_csv = "/opt/airflow/meltano/meltano_project/extract/extract_data_csv.py"
meltano_script_db = "/opt/airflow/meltano/meltano_project/extract/extract_data_db.py"
load_script = "/opt/airflow/meltano/meltano_project/load/load_data_csv_for_db.py"

# Função Python para rodar o script de extração CSV
def run_meltano_script(script_path):
    subprocess.run(["python", script_path], check=True)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 5),
    'retries': 1,
}

with DAG(
    dag_id="extract_postgres_and_csv_data",  # Novo ID para a DAG combinada
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Tarefa para rodar o script de extração de dados do banco via Bash
    extract_task_db = BashOperator(
        task_id="extract_postgres_data",
        bash_command=f"python {meltano_script_db}",
        dag=dag,
    )

    # Tarefa para rodar o script de extração de dados CSV via PythonOperator
    extract_task_csv = PythonOperator(
        task_id="run_meltano_script_csv",
        python_callable=run_meltano_script,
        op_kwargs={"script_path": meltano_script_csv},
        dag=dag,
    )

    load_task = BashOperator(
        task_id='run_load_data_script',
        bash_command="python /opt/airflow/meltano/meltano_project/load/load_data_csv_for_db.py",
        dag=dag,
    )

    # Definir a ordem de execução das tarefas
    extract_task_db >> extract_task_csv >> load_task
