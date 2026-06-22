import sys

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.context import SparkContext
from pyspark.sql.functions import current_timestamp

args = getResolvedOptions(
    sys.argv,
    ['JOB_NAME', 'load_date']
)

load_date = args['load_date']

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args['JOB_NAME'], args)

bucket = "pooja-airline-data-platform"

bronze_path = f"s3://{bucket}/bronze/{load_date}"
silver_path = f"s3://{bucket}/silver/obt"

bookings = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(f"{bronze_path}/bookings.csv")

passengers = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(f"{bronze_path}/passengers.csv")

airports = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(f"{bronze_path}/airports.csv")

silver_df = (
    bookings
    .join(
        passengers,
        "passenger_id",
        "left"
    )
    .join(
        airports,
        "airport_id",
        "left"
    )
)

silver_df = silver_df.withColumn(
    "processed_at",
    current_timestamp()
)

silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(silver_path)

job.commit()