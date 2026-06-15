"""
Silver X users normalizer entry point.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_x_bronze_csv
from src.transformer import transform_x_users
from src.writer import write_users_parquet


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event["bucket_name"]
    x_bronze_key = event["x_bronze_key"]
    x_date = event["x_date"]

    bronze_df = read_x_bronze_csv(bucket_name=bucket_name, object_key=x_bronze_key)
    silver_df = transform_x_users(bronze_df)
    output_path = write_users_parquet(
        df=silver_df,
        bucket_name=bucket_name,
        target_date=x_date,
    )

    return {
        "status": "OK",
        "step": "silver-x-users-normalizer",
        "target_date": x_date,
        "input_rows": len(bronze_df),
        "output_rows": len(silver_df),
        "output_path": output_path,
    }