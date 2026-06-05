"""
Transform raw Hacker News user profiles into normalized silver users records.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
SILVER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if SILVER_ROOT not in sys.path:
    sys.path.append(SILVER_ROOT)

from shared.users_schema import USERS_COLUMNS


def _safe_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def _safe_int(value: Any) -> int | None:
    if value is None or pd.isna(value):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _normalize_timestamp(epoch_value: Any) -> str | None:
    if epoch_value is None or pd.isna(epoch_value):
        return None

    try:
        timestamp = datetime.fromtimestamp(int(epoch_value), tz=timezone.utc)
        return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError, OSError):
        return None


def _build_user_id(username: Any) -> str | None:
    username_str = _safe_string(username)
    if not username_str:
        return None
    return f"hn_{username_str.lower()}"


def transform_hn_users(raw_users: List[Dict[str, Any]]) -> pd.DataFrame:
    records: List[Dict[str, Any]] = []

    for user in raw_users:
        username = _safe_string(user.get("id"))

        record = {
            "user_id": _build_user_id(username),
            "username": username,
            "platform": "HackerNews",
            "created_at": _normalize_timestamp(user.get("created")),
            "karma_score": _safe_int(user.get("karma")),
            "is_verified": None,
            "followers_count": None,
            "friends_count": None,
            "favourites_count": None,
            "location": None,
            "description": _safe_string(user.get("about")),
        }
        records.append(record)

    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(columns=USERS_COLUMNS)

    df = df.dropna(subset=["user_id", "username"])
    df = df.drop_duplicates(subset=["platform", "username"])
    df = df[USERS_COLUMNS]

    return df