"""
Silver Hacker News posts normalizer entry point.

This Lambda should:
- read Bronze Hacker News raw data from S3
- normalize raw items into the shared silver posts schema
- write the result to Silver S3 as partitioned parquet
"""

def lambda_handler(event, context):
    return {
        "status": "NOT_IMPLEMENTED",
        "message": "HN posts normalizer is not implemented yet.",
        "input": event,
    }