"""
AWS Lambda entry point for reading X dataset samples from staging,
filtering by date, and loading into the bronze S3 layer.
"""
import os
import random
import boto3
from .extractor import extract_x_data_for_date

DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")
STAGING_FILE_KEY = os.environ.get("STAGING_FILE_KEY", "bitcoin_tweets_sample.csv")

s3_client = boto3.client("s3")

AVAILABLE_DATES = ["2021-02-08", "2021-02-09", "2021-02-10"]

def lambda_handler(event, context):
    target_date = event.get("target_date")

    if not target_date:
        target_date = random.choice(AVAILABLE_DATES)
        print(f"No target_date provided in event. Randomly selected: {target_date}")

    if not DATA_LAKE_BUCKET or not STAGING_BUCKET:
        raise ValueError("Environment variables for S3 are not set.")

    csv_data, row_count = extract_x_data_for_date(STAGING_BUCKET, STAGING_FILE_KEY, target_date)

    if row_count == 0:
        return {
            "statusCode": 200,
            "message": f"No available data for target date: {target_date}.",
        }

    object_key = f"bronze/x/date={target_date}/x_bronze_{target_date}.csv"

    s3_client.put_object(
        Bucket=DATA_LAKE_BUCKET,
        Key=object_key,
        Body=csv_data.encode('utf-8'),
        ContentType="text/csv"
    )

    summary = {
        "source": "X (Twitter) Dataset",
        "date": target_date,
        "collected_count": row_count,
        "s3_bucket": DATA_LAKE_BUCKET,
        "s3_key": object_key
    }

    print(summary)

    return {
        "statusCode": 200,
        "message": "Bronze X collection completed successfully.",
        "summary": summary
    }