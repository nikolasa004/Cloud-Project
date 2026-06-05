"""
Validate normalized silver datasets.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List

import pandas as pd

CURRENT_DIR = os.path.dirname(__file__)
SILVER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if SILVER_ROOT not in sys.path:
    sys.path.append(SILVER_ROOT)

from shared.posts_schema import POSTS_REQUIRED_COLUMNS
from shared.users_schema import USERS_REQUIRED_COLUMNS


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> List[str]:
    missing = [column for column in required_columns if column not in df.columns]
    return missing


def validate_non_empty(df: pd.DataFrame) -> bool:
    return not df.empty


def build_dataset_result(
    dataset_name: str,
    df: pd.DataFrame,
    required_columns: List[str],
) -> Dict[str, object]:
    missing_columns = validate_required_columns(df, required_columns)
    has_rows = validate_non_empty(df)

    return {
        "dataset_name": dataset_name,
        "row_count": len(df),
        "has_rows": has_rows,
        "missing_columns": missing_columns,
        "is_valid": has_rows and len(missing_columns) == 0,
    }


def validate_silver_outputs(
    hn_posts_df: pd.DataFrame,
    hn_users_df: pd.DataFrame,
    x_posts_df: pd.DataFrame,
    x_users_df: pd.DataFrame,
) -> Dict[str, object]:
    results = [
        build_dataset_result("hn_posts", hn_posts_df, POSTS_REQUIRED_COLUMNS),
        build_dataset_result("hn_users", hn_users_df, USERS_REQUIRED_COLUMNS),
        build_dataset_result("x_posts", x_posts_df, POSTS_REQUIRED_COLUMNS),
        build_dataset_result("x_users", x_users_df, USERS_REQUIRED_COLUMNS),
    ]

    overall_valid = all(result["is_valid"] for result in results)

    return {
        "overall_valid": overall_valid,
        "datasets": results,
    }