"""
Fetch Hacker News user profiles from the official HN API.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Set

import requests

HN_USER_BASE_URL = "https://hacker-news.firebaseio.com/v0/user"
REQUEST_TIMEOUT_SECONDS = 10
MAX_WORKERS = 20


def fetch_user(username: str) -> Optional[Dict[str, Any]]:
    response = requests.get(
        f"{HN_USER_BASE_URL}/{username}.json",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    if payload is None:
        return None
    return payload


def fetch_user_safe(username: str) -> Optional[Dict[str, Any]]:
    try:
        return fetch_user(username)
    except requests.RequestException:
        return None


def fetch_hn_user_profiles(usernames: Set[str]) -> List[Dict[str, Any]]:
    users: List[Dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_user_safe, username): username for username in usernames}

        for future in as_completed(futures):
            user = future.result()
            if user is not None:
                users.append(user)

    return users