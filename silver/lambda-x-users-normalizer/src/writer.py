"""
Write normalized X silver users data to S3 in parquet format.
"""

from __future__ import annotations

import awswrangler as wr
import pandas as pd


def write_users_parquet(
    df: pd.DataFrame,
    bucket_name: str,
    target_date: str,
) -> str:
    output_path = f"s3://{bucket_name}/silver/users/"

    wr.s3.to_parquet(
        df=df,
        path=output_path,
        dataset=True,
        mode="append",
        partition_cols=["platform"],
        filename_prefix=f"x_users_{target_date}_",
    )

    return output_path