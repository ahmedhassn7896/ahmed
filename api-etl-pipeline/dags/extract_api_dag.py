from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests
import json
import logging
import sys

# Ensure plugins can be imported (sys.path insertion is quick fix for mock portfolios)
sys.path.insert(0, '/opt/airflow/plugins') 

from transform_utils import flatten_users_data
from validation import validate_user_data
from sql_queries import CREATE_TABLE_SQL, UPSERT_USERS_SQL

API_URL = "https://randomuser.me/api/?results=100" # Public mock API

def extract_data(**kwargs):
    logging.info("Starting data extraction from API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    raw_data = response.json().get('results', [])
    
    # Passing data to next task via XCom
    kwargs['ti'].xcom_push(key='raw_api_data', value=raw_data)

def transform_and_validate_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_api_data', task_ids='extract_data')
    
    logging.info("Transforming raw data...")
    df = flatten_users_data(raw_data)
    
    logging.info("Validating transformed data...")
    valid_df = validate_user_data(df)
    
    # Save transformed data locally
    file_path = '/tmp/transformed_users.csv'
    valid_df.to_csv(file_path, index=False)
    kwargs['ti'].xcom_push(key='file_path', value=file_path)

def load_to_postgres(**kwargs):
    import pandas as pd
    from psycopg2.extras import execute_values
    
    file_path = kwargs['ti'].xcom_pull(key='file_path', task_ids='transform_and_validate_data')
    df = pd.read_csv(file_path)
    
    hook = PostgresHook(postgres_conn_id='postgres_dwh')
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute(CREATE_TABLE_SQL)
    
    # Prepare tuples for bulk upsert
    data_tuples = [tuple(x) for x in df.to_numpy()]
    execute_values(cursor, UPSERT_USERS_SQL, data_tuples)
    
    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Successfully upserted {len(data_tuples)} records into PostgreSQL.")

default_args = {
    'owner': 'data_engineer',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'api_ingestion_etl',
    default_args=default_args,
    description='A clean daily ETL pipeline from REST API to Postgres',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    t2 = PythonOperator(
        task_id='transform_and_validate_data',
        python_callable=transform_and_validate_data
    )

    t3 = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    t1 >> t2 >> t3
