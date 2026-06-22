import os
import logging
from io import StringIO

import boto3
import pandas as pd
import requests

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class BronzeLayer:

    def __init__(self):

        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.region = os.getenv("AWS_DEFAULT_REGION")

        self.s3_client = boto3.client(
            "s3",
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def ingest_data_api(self, url: str):

        try:

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))

            logging.info(
                f"Successfully fetched data from API. Rows: {len(df)}"
            )

            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            return csv_buffer.getvalue()

        except Exception as e:

            logging.error(f"API ingestion failed: {e}")
            raise

    def upload_to_s3(
        self,
        data: str,
        object_key: str
    ):

        try:

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=data
            )

            logging.info(
                f"Uploaded successfully to s3://{self.bucket_name}/{object_key}"
            )

            return True

        except Exception as e:

            logging.error(f"S3 upload failed: {e}")
            raise

    def validate_upload(self, object_key: str):

        try:

            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            logging.info(
                f"Validation successful for {object_key}"
            )

            return True

        except Exception as e:

            logging.error(f"Validation failed: {e}")
            return False

    def upload_github_file(
        self,
        github_raw_url: str,
        object_key: str
    ):

        data = self.ingest_data_api(github_raw_url)

        self.upload_to_s3(
            data=data,
            object_key=object_key
        )

        self.validate_upload(object_key)