from google.cloud import bigquery
import pandas as pd


def get_bq_client(project_id: str) -> bigquery.Client:
    return bigquery.Client(project=project_id)


def read_table(project_id: str, dataset_id: str, table_name: str) -> pd.DataFrame:
    client = get_bq_client(project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
    return client.query(query).to_dataframe()


def write_dataframe(df: pd.DataFrame, project_id: str, dataset_id: str, table_name: str) -> None:
    client = get_bq_client(project_id)
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
