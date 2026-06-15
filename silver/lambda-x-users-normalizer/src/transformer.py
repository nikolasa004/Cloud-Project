"""
Transform Bronze X raw rows into normalized silver users records.
"""

from __future__ import annotations

import os
import sys
from typing import Any

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
SILVER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if SILVER_ROOT not in sys.path:
    sys.path.append(SILVER_ROOT)

from shared.users_schema import USERS_COLUMNS


def _safe_string(value: Any) -> str | None:
    if pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def _safe_int(value: Any) -> int | None:
    if pd.isna(value):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def _safe_bool(value: Any) -> bool | None:
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


def _normalize_timestamp(value: Any) -> str | None:
    if pd.isna(value):
        return None

    timestamp = pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(timestamp):
        return None

    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_user_id(username: Any) -> str | None:
    username_str = _safe_string(username)
    if not username_str:
        return None

    normalized = username_str.lower().replace(" ", "_")
    return f"x_{normalized}"


def transform_x_users(df: pd.DataFrame) -> pd.DataFrame:
    normalized = pd.DataFrame()

    normalized["user_id"] = df["user_name"].apply(_build_user_id)
    normalized["username"] = df["user_name"].apply(_safe_string)
    normalized["platform"] = "X"
    normalized["created_at"] = df["user_created"].apply(_normalize_timestamp)
    normalized["karma_score"] = None
    normalized["is_verified"] = df["user_verified"].apply(_safe_bool)
    normalized["followers_count"] = df["user_followers"].apply(_safe_int)
    normalized["friends_count"] = df["user_friends"].apply(_safe_int)
    normalized["favourites_count"] = df["user_favourites"].apply(_safe_int)
    normalized["location"] = df["user_location"].apply(_safe_string)
    normalized["description"] = df["user_description"].apply(_safe_string)

    normalized = normalized.dropna(subset=["username"])
    normalized = normalized.drop_duplicates(subset=["platform", "username"])
    normalized = normalized[USERS_COLUMNS]

    return normalized