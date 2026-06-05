"""
Silver Hacker News users normalizer entry point.

This Lambda should:
- read Bronze Hacker News raw data from S3
- extract and deduplicate usernames
- optionally enrich users through the Hacker News user endpoint
- write the result to Silver S3 as partitioned parquet
"""

def lambda_handler(event, context):
    return {
        "status": "NOT_IMPLEMENTED",
        "message": "HN users normalizer is not implemented yet.",
        "input": event,
    }