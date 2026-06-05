"""
Read Bronze X raw CSV files from S3.
"""

from __future__ import annotations

import io

import boto3
import pandas as pd

s3_client = boto3.client("s3")


def read_x_bronze_csv(bucket_name: str, object_key: str) -> pd.DataFrame:
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response["Body"].read().decode("utf-8")
    return pd.read_csv(io.StringIO(content))