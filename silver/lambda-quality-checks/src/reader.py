"""
Read silver parquet datasets from S3 for validation.
"""

from __future__ import annotations

import awswrangler as wr
import pandas as pd


def read_parquet_dataset(path: str) -> pd.DataFrame:
    return wr.s3.read_parquet(path=path, dataset=True)