from __future__ import annotations

import awswrangler as wr
import pandas as pd


def read_silver_users(bucket_name: str, platform: str) -> pd.DataFrame:
    path = f"s3://{bucket_name}/silver/users/platform={platform}/"
    return wr.s3.read_parquet(path=path)