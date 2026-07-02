from __future__ import annotations

from typing import Dict

import awswrangler as wr
import pandas as pd


def load_gold_datasets(bucket_name: str) -> Dict[str, pd.DataFrame]:
    datasets = {}

    dataset_paths = {
        "daily_activity_metric": f"s3://{bucket_name}/gold/daily_activity_metric/",
        "daily_users_metric": f"s3://{bucket_name}/gold/daily_users_metric/",
        "data_quality_kpi": f"s3://{bucket_name}/gold/data_quality_kpi/",
        "top_authors_metric": f"s3://{bucket_name}/gold/top_authors_metric/",
        "top_posts_metric": f"s3://{bucket_name}/gold/top_posts_metric/",
    }

    for table_name, path in dataset_paths.items():
        try:
            datasets[table_name] = wr.s3.read_parquet(path=path)
        except Exception:
            print(f"No data found for {table_name}")
            datasets[table_name] = pd.DataFrame()

    return datasets