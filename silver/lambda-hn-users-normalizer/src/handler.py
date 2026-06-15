"""
Silver Hacker News users normalizer entry point.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_hn_bronze_payload, extract_unique_usernames
from src.enricher import fetch_hn_user_profiles
from src.transformer import transform_hn_users
from src.writer import write_users_parquet


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event["bucket_name"]
    hn_bronze_key = event["hn_bronze_key"]
    hn_date = event["hn_date"]

    bronze_payload = read_hn_bronze_payload(bucket_name=bucket_name, object_key=hn_bronze_key)
    usernames = extract_unique_usernames(bronze_payload)
    raw_users = fetch_hn_user_profiles(usernames)
    silver_df = transform_hn_users(raw_users)

    output_path = write_users_parquet(
        df=silver_df,
        bucket_name=bucket_name,
        hn_date=hn_date,
    )

    return {
        "status": "OK",
        "step": "silver-hn-users-normalizer",
        "hn_date": hn_date,
        "input_usernames": len(usernames),
        "fetched_users": len(raw_users),
        "output_rows": len(silver_df),
        "output_path": output_path,
    }