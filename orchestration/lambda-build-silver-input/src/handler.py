"""
Makes input for Silver layer by combining outputs from Bronze HN and Bronze X Lambdas.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _extract_hn_result(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    for result in results:
        if result.get("date") and result.get("s3_key") and "summary" in result:
            summary = result.get("summary", {})
            type_counts = summary.get("type_counts")
            if isinstance(type_counts, dict):
                return result
    raise ValueError("Hacker News result not found in bronze results.")


def _extract_x_result(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    for result in results:
        summary = result.get("summary", {})
        if summary.get("source") == "X (Twitter) Dataset":
            return result
    raise ValueError("X result not found in bronze results.")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    event = event or {}

    bronze_results = event.get("bronze_results")
    if not bronze_results or not isinstance(bronze_results, list):
        raise ValueError("Expected bronze_results to be a non-empty list.")

    hn_result = _extract_hn_result(bronze_results)
    x_result = _extract_x_result(bronze_results)

    hn_date = hn_result.get("date")
    hn_bronze_key = hn_result.get("s3_key")
    hn_bucket = hn_result.get("s3_bucket")

    x_summary = x_result.get("summary", {})
    x_date = x_summary.get("date")
    x_bronze_key = x_summary.get("s3_key")
    x_bucket = x_summary.get("s3_bucket")

    bucket_name = hn_bucket or x_bucket

    if not bucket_name:
        raise ValueError("bucket_name could not be resolved from bronze outputs.")

    if not hn_date or not hn_bronze_key:
        raise ValueError("Bronze HN output is missing date or s3_key.")

    if not x_date or not x_bronze_key:
        raise ValueError("Bronze X output is missing date or s3_key.")

    return {
        "bucket_name": bucket_name,
        "hn_bronze_key": hn_bronze_key,
        "hn_date": hn_date,
        "x_bronze_key": x_bronze_key,
        "x_date": x_date,
    }