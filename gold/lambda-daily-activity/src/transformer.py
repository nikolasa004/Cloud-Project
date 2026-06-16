from __future__ import annotations

import pandas as pd


def calculate_daily_activity(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    daily_df = df[df["created_at"].dt.strftime("%Y-%m-%d") == target_date].copy()

    is_ask = (daily_df["post_type"] == "story") & (daily_df["title"].str.startswith("Ask HN:", na=False))
    daily_df.loc[is_ask, "post_type"] = "ask"

    counts = daily_df["post_type"].value_counts().to_dict()

    expected_types = ["story", "ask", "comment", "job", "poll"]
    records = []

    for post_type in expected_types:
        records.append({
            "date": target_date,
            "platform": "HackerNews",
            "post_type": post_type,
            "total_count": counts.get(post_type, 0)
        })

    gold_df = pd.DataFrame(records)
    gold_df["date"] = pd.to_datetime(gold_df["date"]).dt.date

    return gold_df