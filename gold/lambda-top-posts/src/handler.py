"""
Gold-layer metric for top-ranked Hacker News posts.

This module will later generate rankings such as:
- top job posts by score
- top story posts by score
"""

from __future__ import annotations

from typing import Any, Dict

from src.reader import read_silver_posts
from src.transformer import calculate_top_posts
from src.writer import write_top_posts


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bucket_name = event.get("bucket_name")
    hn_date = event.get("hn_date")

    if not bucket_name or not hn_date:
        raise ValueError("Missing bucket_name or hn_date in event payload.")

    hn_df = read_silver_posts(bucket_name, "HackerNews")
    
    gold_df = calculate_top_posts(hn_df, hn_date)
    
    output_path = write_top_posts(gold_df, bucket_name)

    return {
        "status": "OK",
        "step": "gold-top-posts",
        "output_path": output_path,
        "metrics": {
            "hn_date": hn_date
        }
    }