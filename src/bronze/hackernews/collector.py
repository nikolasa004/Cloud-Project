"""
Raw Hacker News data collector.

This module will later contain the logic for:
- requesting data from the Hacker News source
- retrieving raw post and user payloads
- preparing raw records for storage in the bronze S3 layer

No transformation or normalization should be performed here.
The bronze layer must preserve the original form of the source data.
"""