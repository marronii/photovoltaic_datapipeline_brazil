from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

#Parametros
default_args ={
    'start_date': datetime(2024, 9, 8)
}

#DAG - Pipeline
dag = DAG("pipeline_aneel_gd", schedule='@monthly', catchup=False,
           default_args=default_args
          )

#Tarefas da Dag
t0 = EmptyOperator(task_id='task0_start', dag=dag)

#Task - Verifica se Existe Arquivo CSV Baixado, caso não realizar download mais recente
t1 = BashOperator(
    task_id='task1_check_and_download_csv', 
    bash_command="""
    if [ -f /opt/airflow/data_raw/empreendimentos.csv ]; then
        echo "Arquivo já existe. Task End."
    else
        curl -o /opt/airflow/data_raw/empreendimentos.csv https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv
    fi
    """, dag=dag)

#Exec - Task
t0 >> t1