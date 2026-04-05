# Planned AWS Resources

## Purpose

This document lists the main AWS resources expected to be used in the project.

## Core Services

### Amazon S3
Used as the main data lake storage layer:
- bronze layer for raw data
- silver layer for normalized parquet datasets
- gold layer for metrics and KPI datasets

### AWS Lambda
Used for serverless data processing:
- Hacker News data collection
- X dataset ingestion support
- silver-layer normalization
- gold-layer metric calculation
- loading metrics into PostgreSQL

### Amazon EC2
Used for hosting:
- PostgreSQL database
- Apache Superset instance

### IAM
Used for:
- defining access permissions
- controlling service access
- enforcing least-privilege access rules

### AWS Step Functions
Can be used to split processing into multiple smaller workflow steps.

### Amazon SNS / Amazon SQS
Can be used for notifications and failed-job handling.

## Additional Notes

- S3 is the main storage foundation of the project.
- Lambda functions are expected to implement most processing stages.
- EC2 is mainly planned for the visualization stack.
- Infrastructure will later be defined through IaC.