"""
Silver quality checks entry point.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_parquet_dataset
from src.validator import validate_silver_outputs


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event["bucket_name"]
    hn_date = event["hn_date"]
    x_date = event["x_date"]

    hn_posts_path = f"s3://{bucket_name}/silver/posts/platform=HackerNews/"
    hn_users_path = f"s3://{bucket_name}/silver/users/platform=HackerNews/"
    x_posts_path = f"s3://{bucket_name}/silver/posts/platform=X/"
    x_users_path = f"s3://{bucket_name}/silver/users/platform=X/"

    hn_posts_df = read_parquet_dataset(hn_posts_path)
    hn_users_df = read_parquet_dataset(hn_users_path)
    x_posts_df = read_parquet_dataset(x_posts_path)
    x_users_df = read_parquet_dataset(x_users_path)

    validation = validate_silver_outputs(
        hn_posts_df=hn_posts_df,
        hn_users_df=hn_users_df,
        x_posts_df=x_posts_df,
        x_users_df=x_users_df,
    )

    if not validation["overall_valid"]:
        raise ValueError(f"Silver quality checks failed: {validation}")

    return {
        "status": "OK",
        "step": "silver-quality-checks",
        "hn_date": hn_date,
        "x_date": x_date,
        "validation": validation,
    }