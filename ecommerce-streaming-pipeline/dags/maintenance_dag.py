from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineer',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Nightly cleanup to remove potential duplicates created by "at-least-once" delivery
with DAG(
    'ecommerce_nightly_maintenance',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    deduplicate_transactions = PostgresOperator(
        task_id='deduplicate_transactions',
        postgres_conn_id='postgres_ecommerce',
        sql="""
            DELETE FROM transactions a 
            USING transactions b 
            WHERE a.ctid < b.ctid 
            AND a.transaction_id = b.transaction_id;
        """
    )
