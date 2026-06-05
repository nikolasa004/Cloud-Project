"""
Validate bronze inputs for the silver normalization workflow.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET", "ftn-social-data-pipeline-2026")


def s3_object_exists(bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name", DATA_LAKE_BUCKET)

    hn_bronze_key = event.get("hn_bronze_key")
    hn_date = event.get("hn_date")

    x_bronze_key = event.get("x_bronze_key")
    x_date = event.get("x_date")

    if not hn_bronze_key:
        raise ValueError("hn_bronze_key is required.")

    if not x_bronze_key:
        raise ValueError("x_bronze_key is required.")

    if not s3_object_exists(bucket_name, hn_bronze_key):
        raise FileNotFoundError(f"Hacker News bronze file not found: s3://{bucket_name}/{hn_bronze_key}")

    if not s3_object_exists(bucket_name, x_bronze_key):
        raise FileNotFoundError(f"X bronze file not found: s3://{bucket_name}/{x_bronze_key}")

    return {
        "bucket_name": bucket_name,
        "hn_bronze_key": hn_bronze_key,
        "hn_date": hn_date,
        "x_bronze_key": x_bronze_key,
        "x_date": x_date,
        "validation_status": "OK",
    }