#!/bin/bash

echo "Deleting Glue Job..."
aws glue delete-job \
    --job-name

echo "Deleting Glue Crawler..."
aws glue delete-crawler \
    --name

echo "Deleting Athena Database..."
aws glue delete-database \
    --name 

echo "Deleting S3 Objects..."
aws s3 rm s3://your-bucket \
    --recursive

echo "Deleting Bucket..."
aws s3 rb s3://your-bucket \
    --force

echo "Done"