"""
Silver X users normalizer entry point.

This Lambda should:
- read Bronze X raw data from S3
- normalize rows into the shared silver users schema
- write the result to Silver S3 as partitioned parquet
"""

def lambda_handler(event, context):
    return {
        "status": "NOT_IMPLEMENTED",
        "message": "X users normalizer is not implemented yet.",
        "input": event,
    }