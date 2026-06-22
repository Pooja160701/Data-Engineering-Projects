import sys

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.context import SparkContext

args = getResolvedOptions(
    sys.argv,
    ['JOB_NAME']
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args['JOB_NAME'], args)

bucket = "pooja-airline-data-platform"

silver_path = f"s3://{bucket}/silver/obt/"
athena_path = f"s3://{bucket}/athena/obt/"

df = spark.read.format("delta").load(
    silver_path
)

df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save(
        athena_path
    )

job.commit()