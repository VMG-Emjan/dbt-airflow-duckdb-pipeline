"""Validate that every DAG in dags/ imports cleanly and is well-formed."""

from pathlib import Path

import pytest
from airflow.models.dagbag import DagBag

DAGS_DIR = Path(__file__).resolve().parent.parent / "dags"


@pytest.fixture(scope="session")
def dagbag() -> DagBag:
    return DagBag(dag_folder=str(DAGS_DIR), include_examples=False)


def test_no_import_errors(dagbag: DagBag) -> None:
    assert dagbag.import_errors == {}, f"DAG import errors: {dagbag.import_errors}"


def test_expected_dag_is_present(dagbag: DagBag) -> None:
    assert "dbt_duckdb_pipeline" in dagbag.dags


def test_pipeline_task_order(dagbag: DagBag) -> None:
    dag = dagbag.dags["dbt_duckdb_pipeline"]
    task_ids = [t.task_id for t in dag.topological_sort()]
    assert task_ids == ["dbt_seed", "dbt_run", "dbt_test", "dbt_docs_generate"]


def test_dag_has_no_cycles_and_retries(dagbag: DagBag) -> None:
    dag = dagbag.dags["dbt_duckdb_pipeline"]
    assert dag.catchup is False
    for task in dag.tasks:
        assert task.retries >= 1
