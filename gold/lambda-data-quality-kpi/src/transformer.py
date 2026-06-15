from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


def _calculate_score(df: pd.DataFrame, target_date: str) -> float:
    if df.empty:
        return 100.0

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    daily_df = df[df["created_at"].dt.strftime("%Y-%m-%d") == target_date]

    if daily_df.empty:
        return 100.0

    total_rows = len(daily_df)
    valid_rows = len(daily_df.dropna())
    
    score = (valid_rows / total_rows) * 100
    return round(score, 2)


def calculate_quality_kpi(
    hn_posts: pd.DataFrame, 
    hn_users: pd.DataFrame, 
    x_posts: pd.DataFrame, 
    x_users: pd.DataFrame, 
    hn_date: str, 
    x_date: str
) -> pd.DataFrame:
    records = [
        {
            "date": hn_date,
            "platform": "HackerNews",
            "dataset": "posts",
            "quality_score_percent": _calculate_score(hn_posts, hn_date)
        },
        {
            "date": hn_date,
            "platform": "HackerNews",
            "dataset": "users",
            "quality_score_percent": _calculate_score(hn_users, hn_date)
        },
        {
            "date": x_date,
            "platform": "X",
            "dataset": "posts",
            "quality_score_percent": _calculate_score(x_posts, x_date)
        },
        {
            "date": x_date,
            "platform": "X",
            "dataset": "users",
            "quality_score_percent": _calculate_score(x_users, x_date)
        }
    ]

    gold_df = pd.DataFrame(records)
    gold_df["date"] = pd.to_datetime(gold_df["date"]).dt.date

    return gold_df