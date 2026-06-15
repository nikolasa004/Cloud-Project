from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


def _build_records(df: pd.DataFrame, date: str, category: str) -> List[Dict[str, Any]]:
    records = []
    rank = 1
    for _, row in df.iterrows():
        records.append({
            "date": date,
            "platform": "HackerNews",
            "category": category,
            "rank": rank,
            "post_id": row.get("post_id"),
            "author_username": row.get("author_username"),
            "title": row.get("title"),
            "score": int(row.get("score"))
        })
        rank += 1
    return records


def calculate_top_posts(hn_df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    hn_df["created_at_dt"] = pd.to_datetime(hn_df["created_at"], errors="coerce")
    daily_df = hn_df[hn_df["created_at_dt"].dt.strftime("%Y-%m-%d") == target_date].copy()

    daily_df = daily_df.dropna(subset=["score"])
    daily_df["score"] = pd.to_numeric(daily_df["score"], errors="coerce")

    jobs_df = daily_df[daily_df["post_type"] == "job"]
    top_jobs = jobs_df.nlargest(10, "score")

    stories_df = daily_df[daily_df["post_type"] == "story"]
    top_stories = stories_df.nlargest(10, "score")

    all_records = []
    all_records.extend(_build_records(top_jobs, target_date, "highest_job_score"))
    all_records.extend(_build_records(top_stories, target_date, "highest_story_score"))

    gold_df = pd.DataFrame(all_records)
    
    if not gold_df.empty:
        gold_df["date"] = pd.to_datetime(gold_df["date"]).dt.date
    else:
        gold_df = pd.DataFrame(columns=[
            "date", "platform", "category", "rank", "post_id", "author_username", "title", "score"
        ])

    return gold_df