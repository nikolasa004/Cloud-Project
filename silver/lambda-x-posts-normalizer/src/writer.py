"""
Write normalized X silver posts data to S3 in parquet format.
"""

from __future__ import annotations

from typing import Any

import awswrangler as wr
import pandas as pd


def write_posts_parquet(
    df: pd.DataFrame,
    bucket_name: str,
    target_date: str,
) -> str:
    year, month, day = target_date.split("-")

    output_path = f"s3://{bucket_name}/silver/posts/"

    wr.s3.to_parquet(
        df=df,
        path=output_path,
        dataset=True,
        mode="append",
        partition_cols=["platform"],
        filename_prefix=f"x_posts_{year}_{month}_{day}_",
    )

    return output_path