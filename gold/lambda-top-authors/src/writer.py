from __future__ import annotations

import awswrangler as wr
import pandas as pd


def write_top_authors(df: pd.DataFrame, bucket_name: str) -> str:
    output_path = f"s3://{bucket_name}/gold/top_authors_metric/"

    if df.empty:
        return output_path

    wr.s3.to_parquet(
        df=df,
        path=output_path,
        dataset=True,
        partition_cols=["platform", "date"],
        mode="overwrite_partitions"
    )

    return output_path