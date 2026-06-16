from __future__ import annotations

from typing import Any, Dict

from src.reader import read_silver_dataset
from src.transformer import calculate_quality_kpi
from src.writer import write_quality_kpi


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")
    hn_date = event.get("hn_date")
    x_date = event.get("x_date")

    if not bucket_name or not hn_date or not x_date:
        raise ValueError("Missing required parameters in event payload.")

    hn_posts = read_silver_dataset(bucket_name, "posts", "HackerNews")
    hn_users = read_silver_dataset(bucket_name, "users", "HackerNews")
    
    x_posts = read_silver_dataset(bucket_name, "posts", "X")
    x_users = read_silver_dataset(bucket_name, "users", "X")

    gold_df = calculate_quality_kpi(
        hn_posts=hn_posts, 
        hn_users=hn_users, 
        x_posts=x_posts, 
        x_users=x_users, 
        hn_date=hn_date, 
        x_date=x_date
    )

    output_path = write_quality_kpi(gold_df, bucket_name)

    return {
        "status": "OK",
        "step": "gold-data-quality-kpi",
        "output_path": output_path
    }