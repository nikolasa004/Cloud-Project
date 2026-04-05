# Infrastructure

This folder is reserved for Infrastructure as Code (IaC) files.

According to the project specification, the complete AWS infrastructure must be defined using an IaC tool such as:
- AWS CDK
- CloudFormation
- Terraform
- Terragrunt

The final infrastructure definition will include resources such as:
- S3 buckets for bronze, silver, and gold layers
- Lambda functions for ingestion, normalization, transformation, and loading
- IAM roles and permissions
- VPC and security groups
- EC2 instance for PostgreSQL and Apache Superset
- optional Step Functions and notification resources

IaC implementation is intentionally postponed until the corresponding course topics are covered.