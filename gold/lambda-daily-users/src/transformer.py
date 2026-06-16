from __future__ import annotations

import pandas as pd


def calculate_daily_users(
    hn_df: pd.DataFrame, 
    x_df: pd.DataFrame, 
    hn_date: str, 
    x_date: str
) -> pd.DataFrame:
    hn_df["created_at"] = pd.to_datetime(hn_df["created_at"], errors="coerce")
    x_df["created_at"] = pd.to_datetime(x_df["created_at"], errors="coerce")

    hn_total = len(hn_df)
    hn_new = len(hn_df[hn_df["created_at"].dt.strftime("%Y-%m-%d") == hn_date])

    x_total = len(x_df)
    x_new = len(x_df[x_df["created_at"].dt.strftime("%Y-%m-%d") == x_date])

    gold_df = pd.DataFrame({
        "date": [hn_date, x_date],
        "platform": ["HackerNews", "X"],
        "total_users": [hn_total, x_total],
        "new_users": [hn_new, x_new],
    })

    gold_df["date"] = pd.to_datetime(gold_df["date"]).dt.date

    return gold_df