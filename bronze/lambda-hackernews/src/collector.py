"""
Raw Hacker News data collector.

This module contains the logic for:
- requesting data from the Hacker News source
- retrieving raw post and user payloads
- preparing raw records for storage in the bronze S3 layer

No transformation or normalization should be performed here.
The bronze layer must preserve the original form of the source data.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

import requests


HN_ITEM_BASE_URL = "https://hacker-news.firebaseio.com/v0/item"
ALGOLIA_SEARCH_URL = "https://hn.algolia.com/api/v1/search_by_date"

REQUEST_TIMEOUT_SECONDS = 10
MAX_WORKERS = 20

ALLOWED_TYPES = {"story", "comment", "job", "poll"}
ALGOLIA_TAGS = ["story", "comment", "job", "poll", "ask_hn"]


def get_previous_day_range_utc(reference_dt: Optional[datetime] = None) -> tuple[int, int, str]:
    if reference_dt is None:
        reference_dt = datetime.now(timezone.utc)

    current_day_start = datetime(
        year=reference_dt.year,
        month=reference_dt.month,
        day=reference_dt.day,
        tzinfo=timezone.utc,
    )
    previous_day_start = current_day_start - timedelta(days=1)

    start_ts = int(previous_day_start.timestamp())
    end_ts = int(current_day_start.timestamp())
    date_label = previous_day_start.strftime("%Y-%m-%d")

    return start_ts, end_ts, date_label


def fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Any:
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def fetch_algolia_ids_for_tag(tag: str, start_ts: int, end_ts: int) -> Set[int]:
    ids: Set[int] = set()
    page = 0

    while True:
        payload = fetch_json(
            ALGOLIA_SEARCH_URL,
            params={
                "tags": tag,
                "numericFilters": f"created_at_i>={start_ts},created_at_i<{end_ts}",
                "hitsPerPage": 1000,
                "page": page,
            },
        )

        hits = payload.get("hits", [])
        for hit in hits:
            object_id = hit.get("objectID")
            if object_id and str(object_id).isdigit():
                ids.add(int(object_id))

        nb_pages = payload.get("nbPages", 0)
        page += 1
        if page >= nb_pages:
            break

    return ids


def fetch_item(item_id: int) -> Optional[Dict[str, Any]]:
    item = fetch_json(f"{HN_ITEM_BASE_URL}/{item_id}.json")
    if item is None:
        return None
    return item


def fetch_item_safe(item_id: int) -> Optional[Dict[str, Any]]:
    try:
        return fetch_item(item_id)
    except requests.RequestException:
        return None


def collect_previous_day_hn_items(reference_dt: Optional[datetime] = None) -> Dict[str, Any]:
    start_ts, end_ts, date_label = get_previous_day_range_utc(reference_dt)

    collected_ids: Set[int] = set()
    for tag in ALGOLIA_TAGS:
        collected_ids.update(fetch_algolia_ids_for_tag(tag, start_ts, end_ts))

    raw_items: List[Dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_item_safe, item_id): item_id for item_id in collected_ids}

        for future in as_completed(futures):
            item = future.result()
            if item is None:
                continue

            item_type = item.get("type")
            item_time = item.get("time")

            if item_type not in ALLOWED_TYPES:
                continue

            if not isinstance(item_time, int):
                continue

            if not (start_ts <= item_time < end_ts):
                continue

            raw_items.append(item)

    raw_items.sort(key=lambda x: x.get("time", 0))

    return {
        "source": "Hacker News",
        "date": date_label,
        "window_start_utc": start_ts,
        "window_end_utc": end_ts,
        "collected_count": len(raw_items),
        "items": raw_items,
    }