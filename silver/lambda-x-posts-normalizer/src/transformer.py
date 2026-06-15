"""
Transform Bronze X raw rows into normalized silver posts records.
"""

from __future__ import annotations

import hashlib
import os
import sys
from typing import Any

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
SILVER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if SILVER_ROOT not in sys.path:
    sys.path.append(SILVER_ROOT)

from shared.posts_schema import POSTS_COLUMNS

def _safe_string(value: Any) -> str | None:
    if pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def _normalize_timestamp(value: Any) -> str | None:
    if pd.isna(value):
        return None

    timestamp = pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(timestamp):
        return None

    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_hashtags(value: Any) -> str | None:
    if pd.isna(value):
        return None

    value = str(value).strip()
    if not value:
        return None

    value = value.strip("[]")
    value = value.replace("'", "").replace('"', "")
    value = value.strip()

    return value if value else None


def _normalize_boolean(value: Any) -> bool | None:
    if pd.isna(value):
        return None

    if isinstance(value, bool):
        return value

    value_str = str(value).strip().lower()
    if value_str in {"true", "1", "yes"}:
        return True
    if value_str in {"false", "0", "no"}:
        return False

    return None


def _build_post_id(row: pd.Series) -> str:
    raw_value = f"{row.get('user_name','')}|{row.get('date','')}|{row.get('text','')}"
    return hashlib.sha256(str(raw_value).encode("utf-8")).hexdigest()


def transform_x_posts(df: pd.DataFrame) -> pd.DataFrame:
    normalized = pd.DataFrame()

    normalized["post_id"] = df.apply(_build_post_id, axis=1)
    normalized["author_username"] = df["user_name"].apply(_safe_string)
    normalized["platform"] = "X"
    normalized["content_text"] = df["text"].apply(_safe_string)
    normalized["created_at"] = df["date"].apply(_normalize_timestamp)
    normalized["post_type"] = df["is_retweet"].apply(
        lambda x: "retweet" if _normalize_boolean(x) is True else "tweet"
    )
    normalized["title"] = None
    normalized["score"] = None
    normalized["comment_count"] = None
    normalized["hashtags"] = df["hashtags"].apply(_normalize_hashtags)
    normalized["url"] = None
    normalized["source"] = df["source"].apply(_safe_string)
    normalized["is_retweet"] = df["is_retweet"].apply(_normalize_boolean)

    normalized = normalized.drop_duplicates(subset=["post_id"])
    normalized = normalized[POSTS_COLUMNS]

    return normalized