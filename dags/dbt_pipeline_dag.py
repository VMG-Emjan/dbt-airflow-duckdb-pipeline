"""Daily dbt pipeline: seed -> run -> test -> docs.

Each task shells out to dbt Core against the local DuckDB warehouse.
The DAG is intentionally linear: every step must succeed before the
next one runs, so a failed test blocks the docs build.
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG

try:  # Airflow 3.x
    from airflow.providers.standard.operators.bash import BashOperator
except ImportError:  # Airflow 2.x
    from airflow.operators.bash import BashOperator

PROJECT_DIR = Path(__file__).resolve().parent.parent

DBT = f"dbt --no-use-colors {{}} --project-dir {PROJECT_DIR} --profiles-dir {PROJECT_DIR}"

default_args = {
    "owner": "data-eng",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dbt_duckdb_pipeline",
    description="Seed, build, test and document the DuckDB warehouse with dbt",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dbt", "duckdb", "analytics"],
) as dag:
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=DBT.format("seed"),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=DBT.format("run"),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=DBT.format("test"),
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=DBT.format("docs generate"),
    )

    dbt_seed >> dbt_run >> dbt_test >> dbt_docs
