import boto3

def test_s3_connection():
    s3 = boto3.client("s3")

    response = s3.list_objects_v2(
        Bucket="pooja-airline-data-platform",
        Prefix="bronze/"
    )

    assert "Contents" in response