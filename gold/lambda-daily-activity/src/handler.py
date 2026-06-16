"""
Gold-layer metric for daily Hacker News activity.

This module will later calculate daily counts of different Hacker News post types,
such as stories, asks, comments, jobs, and polls.
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_silver_posts
from src.transformer import calculate_daily_activity
from src.writer import write_daily_activity


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")
    hn_date = event.get("hn_date")

    if not bucket_name or not hn_date:
        raise ValueError("Missing bucket_name or hn_date in event payload.")

    hn_df = read_silver_posts(bucket_name, "HackerNews")
    
    gold_df = calculate_daily_activity(hn_df, hn_date)
    
    output_path = write_daily_activity(gold_df, bucket_name)

    return {
        "status": "OK",
        "step": "gold-daily-activity",
        "output_path": output_path,
        "metrics": {
            "hn_date": hn_date
        }
    }