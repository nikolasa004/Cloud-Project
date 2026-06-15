from __future__ import annotations

import awswrangler as wr
import pandas as pd


def read_silver_dataset(bucket_name: str, dataset_type: str, platform: str) -> pd.DataFrame:
    path = f"s3://{bucket_name}/silver/{dataset_type}/platform={platform}/"
    try:
        return wr.s3.read_parquet(path=path)
    except Exception:
        return pd.DataFrame()