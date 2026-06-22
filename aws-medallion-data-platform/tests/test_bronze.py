import os
import sys

sys.path.append("/opt/airflow")

from utils.bronze_layer import BronzeLayer

URL = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"

bronze = BronzeLayer()

data = bronze.ingest_data_api(URL)

object_key = "bronze/test/countries.csv"

bronze.upload_to_s3(
    data=data,
    object_key=object_key
)

bronze.validate_upload(object_key)