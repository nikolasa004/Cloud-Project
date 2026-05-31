"""
Data extractor for X (Twitter) networks from Staging S3 bucket.
Separates reading and filtering logic from AWS Lambda handler.
"""
import csv
import io
import boto3

s3_client = boto3.client("s3")

def extract_x_data_for_date(staging_bucket: str, file_key: str, target_date: str) -> tuple[str, int]:
    """
    Extracts CSV from Staging bucket, filters it by date and returns the filtered string.
    """

    response = s3_client.get_object(Bucket=staging_bucket, Key=file_key)
    lines = response['Body'].read().decode('utf-8').splitlines()


    reader = csv.DictReader(lines)
    fieldnames = reader.fieldnames


    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    count = 0

    for row in reader:
        if row.get('date', '').startswith(target_date):
            writer.writerow(row)
            count += 1

    return output.getvalue(), count