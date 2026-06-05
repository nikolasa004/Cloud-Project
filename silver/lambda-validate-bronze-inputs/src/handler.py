"""
Validate bronze inputs for the silver normalization workflow.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET", "ftn-social-data-pipeline-2026")


def get_default_target_date() -> str:
    now_utc = datetime.now(timezone.utc)
    previous_day = now_utc.date() - timedelta(days=1)
    return previous_day.isoformat()


def validate_date_string(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def s3_object_exists(bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    target_date = event.get("target_date", get_default_target_date())
    if not validate_date_string(target_date):
        raise ValueError(f"Invalid target_date format: {target_date}. Expected YYYY-MM-DD.")

    hn_bronze_key = event.get(
        "hn_bronze_key",
        f"bronze/hackernews/date={target_date}/hn_bronze_{target_date}.json",
    )
    x_bronze_key = event.get(
        "x_bronze_key",
        f"bronze/x/date={target_date}/x_bronze_{target_date}.csv",
    )

    hn_exists = s3_object_exists(DATA_LAKE_BUCKET, hn_bronze_key)
    x_exists = s3_object_exists(DATA_LAKE_BUCKET, x_bronze_key)

    if not hn_exists:
        raise FileNotFoundError(f"Hacker News bronze file not found: s3://{DATA_LAKE_BUCKET}/{hn_bronze_key}")

    if not x_exists:
        raise FileNotFoundError(f"X bronze file not found: s3://{DATA_LAKE_BUCKET}/{x_bronze_key}")

    return {
        "target_date": target_date,
        "bucket_name": DATA_LAKE_BUCKET,
        "hn_bronze_key": hn_bronze_key,
        "x_bronze_key": x_bronze_key,
        "validation_status": "OK",
    }