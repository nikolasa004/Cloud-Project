"""
Transform Bronze Hacker News raw items into normalized silver posts records.
"""

from __future__ import annotations

import html
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
SILVER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if SILVER_ROOT not in sys.path:
    sys.path.append(SILVER_ROOT)

from shared.posts_schema import POSTS_COLUMNS


HTML_TAG_RE = re.compile(r"<[^>]+>")


def _safe_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def _normalize_timestamp(epoch_value: Any) -> str | None:
    if epoch_value is None or pd.isna(epoch_value):
        return None

    try:
        timestamp = datetime.fromtimestamp(int(epoch_value), tz=timezone.utc)
        return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError, OSError):
        return None


def _clean_text(value: Any) -> str | None:
    text = _safe_string(value)
    if not text:
        return None

    text = html.unescape(text)
    text = HTML_TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text if text else None


def _normalize_post_type(value: Any) -> str | None:
    post_type = _safe_string(value)
    if not post_type:
        return None

    allowed = {"story", "comment", "job", "poll"}
    return post_type if post_type in allowed else None


def transform_hn_posts(payload: Dict[str, Any]) -> pd.DataFrame:
    items: List[Dict[str, Any]] = payload.get("items", [])

    records: List[Dict[str, Any]] = []

    for item in items:
        record = {
            "post_id": str(item.get("id")) if item.get("id") is not None else None,
            "author_username": _safe_string(item.get("by")),
            "platform": "HackerNews",
            "content_text": _clean_text(item.get("text")),
            "created_at": _normalize_timestamp(item.get("time")),
            "post_type": _normalize_post_type(item.get("type")),
            "title": _clean_text(item.get("title")),
            "score": item.get("score"),
            "comment_count": item.get("descendants"),
            "hashtags": None,
            "url": _safe_string(item.get("url")),
            "source": "HackerNews",
            "is_retweet": None,
        }
        records.append(record)

    df = pd.DataFrame(records)

    if df.empty:
        df = pd.DataFrame(columns=POSTS_COLUMNS)
        return df

    df = df.dropna(subset=["post_id", "author_username", "created_at", "post_type"])
    df = df.drop_duplicates(subset=["post_id"])
    df = df[POSTS_COLUMNS]

    return df