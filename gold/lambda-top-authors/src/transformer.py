from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


def _build_records(df: pd.DataFrame, date: str, platform: str, category: str, score_col: str) -> List[Dict[str, Any]]:
    records = []
    rank = 1
    for _, row in df.iterrows():
        records.append({
            "date": date,
            "platform": platform,
            "category": category,
            "rank": rank,
            "username": row.get("username"),
            "score": int(row.get(score_col))
        })
        rank += 1
    return records


def calculate_top_authors(hn_df: pd.DataFrame, x_df: pd.DataFrame, hn_date: str, x_date: str) -> pd.DataFrame:
    all_records = []

    x_clean = x_df.dropna(subset=["followers_count"]).copy()
    x_clean["followers_count"] = pd.to_numeric(x_clean["followers_count"], errors="coerce")
    top_x = x_clean.nlargest(10, "followers_count")
    
    all_records.extend(_build_records(top_x, x_date, "X", "most_followers", "followers_count"))

    hn_clean = hn_df.dropna(subset=["karma_score"]).copy()
    hn_clean["karma_score"] = pd.to_numeric(hn_clean["karma_score"], errors="coerce")
    
    top_hn_high = hn_clean.nlargest(10, "karma_score")
    all_records.extend(_build_records(top_hn_high, hn_date, "HackerNews", "highest_karma", "karma_score"))

    top_hn_low = hn_clean.nsmallest(10, "karma_score")
    all_records.extend(_build_records(top_hn_low, hn_date, "HackerNews", "lowest_karma", "karma_score"))

    gold_df = pd.DataFrame(all_records)
    
    if not gold_df.empty:
        gold_df["date"] = pd.to_datetime(gold_df["date"]).dt.date
    else:
        gold_df = pd.DataFrame(columns=["date", "platform", "category", "rank", "username", "score"])

    return gold_df