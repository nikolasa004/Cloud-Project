"""
Gold-layer metric for daily platform user counts.

This module will later calculate daily user metrics for Hacker News and X,
including total users and newly observed users per day.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_silver_users
from src.transformer import calculate_daily_users
from src.writer import write_daily_users


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")
    hn_date = event.get("hn_date")
    x_date = event.get("x_date")

    if not bucket_name or not hn_date or not x_date:
        raise ValueError("Missing bucket_name, hn_date, or x_date in event payload.")

    hn_df = read_silver_users(bucket_name, "HackerNews")
    x_df = read_silver_users(bucket_name, "X")

    gold_df = calculate_daily_users(hn_df, x_df, hn_date, x_date)

    output_path = write_daily_users(gold_df, bucket_name)

    return {
        "status": "OK",
        "step": "gold-daily-users",
        "output_path": output_path,
        "metrics": {
            "hn_date": hn_date,
            "x_date": x_date
        }
    }