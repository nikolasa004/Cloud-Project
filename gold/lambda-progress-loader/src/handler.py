from __future__ import annotations

from typing import Any, Dict

from src.reader import load_gold_datasets
from src.postgres import upload_to_postgres


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")

    if not bucket_name:
        raise ValueError("Missing bucket_name in event payload.")

    datasets = load_gold_datasets(bucket_name)

    total_rows = upload_to_postgres(datasets)

    return {
        "status": "OK",
        "step": "gold-progress-loader",
        "datasets_loaded": len(datasets),
        "rows_loaded": total_rows
    }