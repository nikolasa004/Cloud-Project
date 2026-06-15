"""
Gold-layer metric for top-ranked platform users.

This module will later generate rankings such as:
- top X users by follower count
- top Hacker News users by highest karma score
- top Hacker News users by lowest karma score
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_silver_users
from src.transformer import calculate_top_authors
from src.writer import write_top_authors


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")
    hn_date = event.get("hn_date")
    x_date = event.get("x_date")

    if not bucket_name or not hn_date or not x_date:
        raise ValueError("Missing bucket_name, hn_date, or x_date in event payload.")

    hn_df = read_silver_users(bucket_name, "HackerNews")
    x_df = read_silver_users(bucket_name, "X")

    gold_df = calculate_top_authors(hn_df, x_df, hn_date, x_date)

    output_path = write_top_authors(gold_df, bucket_name)

    return {
        "status": "OK",
        "step": "gold-top-authors",
        "output_path": output_path,
        "metrics": {
            "hn_date": hn_date,
            "x_date": x_date
        }
    }