from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

from datetime import datetime, timedelta

import sys

sys.path.append("/opt/airflow")

from utils.bronze_layer import BronzeLayer


# -------------------------------
# Bronze Upload
# -------------------------------

def bronze_ingestion():

    urls = [

        "https://raw.githubusercontent.com/Pooja160701/Data-Engineering-Projects/refs/heads/main/aws-medallion-data-platform/datasets/bookings.csv",

        "https://raw.githubusercontent.com/Pooja160701/Data-Engineering-Projects/refs/heads/main/aws-medallion-data-platform/datasets/airports.csv",

        "https://raw.githubusercontent.com/Pooja160701/Data-Engineering-Projects/refs/heads/main/aws-medallion-data-platform/datasets/passengers.csv"
    ]

    folder_name = datetime.now().strftime("%Y-%m-%d")

    bronze = BronzeLayer()

    for url in urls:

        file_name = url.split("/")[-1]

        bronze.upload_github_file(
            github_raw_url=url,
            object_key=f"bronze/{folder_name}/{file_name}"
        )


# -------------------------------
# DAG
# -------------------------------

default_args = {
    "owner": "pooja",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    dag_id="aws_project",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["aws", "medallion"]
) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_ingestion",
        python_callable=bronze_ingestion
    )

    silver_task = GlueJobOperator(
        task_id="run_silver_glue_job",
        job_name="silver_layer",
        wait_for_completion=True,
        aws_conn_id="aws_default",
        region_name="ap-south-1"
    )

    crawler_task = GlueCrawlerOperator(
        task_id="run_crawler",
        config={
            "Name": "crawler_silver"
        }
    )

    athena_validation = AthenaOperator(
        task_id="validate_silver_data",
        query="""
        SELECT COUNT(*)
        FROM airline_db.obt
        """,
        database="airline_db",
        output_location="s3://pooja-airline-data-platform/athena/results/"
    )

    run_gold_databricks = DatabricksRunNowOperator(
        task_id="run_gold_databricks",
        databricks_conn_id="databricks_default",
        job_id=607843697110998
    )

    bronze_task >> silver_task >> crawler_task >> athena_validation >> run_gold_databricks