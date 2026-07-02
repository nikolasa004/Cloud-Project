from __future__ import annotations

import awswrangler as wr
import pandas as pd


def read_daily_activity(bucket_name: str) -> pd.DataFrame:
    return wr.s3.read_parquet(
        path=f"s3://{bucket_name}/gold/daily_activity_metric/"
    )


def read_daily_users(bucket_name: str) -> pd.DataFrame:
    return wr.s3.read_parquet(
        path=f"s3://{bucket_name}/gold/daily_users_metric/"
    )


def read_top_authors(bucket_name: str) -> pd.DataFrame:
    return wr.s3.read_parquet(
        path=f"s3://{bucket_name}/gold/top_authors_metric/"
    )


def read_top_posts(bucket_name: str) -> pd.DataFrame:
    return wr.s3.read_parquet(
        path=f"s3://{bucket_name}/gold/top_posts_metric/"
    )


def read_data_quality(bucket_name: str) -> pd.DataFrame:
    return wr.s3.read_parquet(
        path=f"s3://{bucket_name}/gold/data_quality_metric/"
    )