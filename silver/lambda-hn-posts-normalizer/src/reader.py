"""
Read Bronze Hacker News raw JSON payloads from S3.
"""

from __future__ import annotations

import json
from typing import Any, Dict

import boto3

s3_client = boto3.client("s3")


def read_hn_bronze_payload(bucket_name: str, object_key: str) -> Dict[str, Any]:
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response["Body"].read().decode("utf-8")
    return json.loads(content)