from airflow.sdk import dag, task


@dag(
    schedule="@daily",
    catchup=False
)
def aws_project():

    @task
    def test_task():
        print("Airflow is working")

    test_task()


aws_project()