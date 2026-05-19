"""
AWS Lambda entry point for collecting raw Hacker News data
and storing it in the bronze S3 layer.
"""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict

import boto3

from .collector import collect_previous_day_hn_items


BUCKET_NAME = os.environ.get("BUCKET_NAME")

s3_client = boto3.client("s3")


def build_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("items", [])

    type_counter = Counter()
    timestamps = []

    for item in items:
        item_type = item.get("type")
        item_time = item.get("time")

        if isinstance(item_type, str):
            type_counter[item_type] += 1

        if isinstance(item_time, int):
            timestamps.append(item_time)

    earliest_utc = None
    latest_utc = None

    if timestamps:
        earliest_utc = datetime.fromtimestamp(min(timestamps), tz=timezone.utc).isoformat()
        latest_utc = datetime.fromtimestamp(max(timestamps), tz=timezone.utc).isoformat()

    return {
        "date": payload.get("date"),
        "collected_count": payload.get("collected_count", 0),
        "type_counts": dict(type_counter),
        "earliest_item_utc": earliest_utc,
        "latest_item_utc": latest_utc,
    }


def upload_to_s3(payload: Dict[str, Any]) -> str:
    if not BUCKET_NAME:
        raise ValueError("BUCKET_NAME is not set.")

    date_label = payload["date"]
    object_key = f"bronze/hackernews/date={date_label}/hn_bronze_{date_label}.json"

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    return object_key


def lambda_handler(event, context):
    payload = collect_previous_day_hn_items()
    summary = build_summary(payload)
    object_key = upload_to_s3(payload)

    print(json.dumps(summary, indent=2))

    return {
        "statusCode": 200,
        "message": "Bronze Hacker News collection completed successfully.",
        "date": payload["date"],
        "collected_count": payload["collected_count"],
        "s3_bucket": BUCKET_NAME,
        "s3_key": object_key,
        "summary": summary,
    }