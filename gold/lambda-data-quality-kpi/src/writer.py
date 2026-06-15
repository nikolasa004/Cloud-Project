from __future__ import annotations

import awswrangler as wr
import pandas as pd


def write_quality_kpi(df: pd.DataFrame, bucket_name: str) -> str:
    output_path = f"s3://{bucket_name}/gold/data_quality_kpi/"

    wr.s3.to_parquet(
        df=df,
        path=output_path,
        dataset=True,
        partition_cols=["platform", "date"],
        mode="overwrite_partitions"
    )

    return output_path