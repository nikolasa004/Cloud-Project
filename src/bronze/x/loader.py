"""
Raw X dataset loader.

This module will later contain the logic for:
- reading an external X dataset
- validating the raw input format
- storing raw dataset records in the bronze S3 layer

No normalization should be applied here.
The bronze layer must preserve source data in its original form.
"""