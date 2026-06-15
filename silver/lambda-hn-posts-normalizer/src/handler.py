"""
Silver Hacker News posts normalizer entry point.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_hn_bronze_payload
from src.transformer import transform_hn_posts
from src.writer import write_posts_parquet


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event["bucket_name"]
    hn_bronze_key = event["hn_bronze_key"]
    hn_date = event["hn_date"]

    bronze_payload = read_hn_bronze_payload(bucket_name=bucket_name, object_key=hn_bronze_key)
    silver_df = transform_hn_posts(bronze_payload)
    output_path = write_posts_parquet(
        df=silver_df,
        bucket_name=bucket_name,
        target_date=hn_date,
    )

    return {
        "status": "OK",
        "step": "silver-hn-posts-normalizer",
        "target_date": hn_date,
        "input_rows": len(bronze_payload.get("items", [])),
        "output_rows": len(silver_df),
        "output_path": output_path,
    }