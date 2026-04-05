# Architecture Overview

## Project Goal

The goal of this project is to implement an AWS-based platform for collecting, processing, storing, and analyzing data from social media and blog-related sources.

The solution follows the medallion architecture:
- **Bronze layer** - raw data ingestion
- **Silver layer** - normalized and cleaned data
- **Gold layer** - business metrics and KPIs

According to the project specification, the platform uses two data sources:
- **Hacker News**
- **X (Twitter) dataset**

## High-Level Architecture

The processing flow is organized into four logical stages:

1. **Bronze**
   - collect raw Hacker News data
   - import X dataset into the data lake
   - store everything in Amazon S3 without transformation

2. **Silver**
   - normalize data from both sources
   - align timestamps into a single UTC format
   - clean text values
   - remove duplicates
   - define a usable data schema
   - store normalized data in parquet format

3. **Gold**
   - calculate metrics and KPIs from silver-layer datasets
   - prepare business-oriented outputs for analytics

4. **Serving / Visualization support**
   - move gold-layer metrics from S3 to PostgreSQL
   - expose the data to Apache Superset for dashboard creation

## Planned AWS Services

The project is expected to use the following AWS services:
- **Amazon S3** for data lake storage
- **AWS Lambda** for ingestion, normalization, transformation, and loading
- **Amazon EC2** for hosting PostgreSQL and Apache Superset
- **IAM** for access control
- **Step Functions** as an optional orchestration mechanism
- **SNS / SQS** or another notification mechanism for failed jobs

## Infrastructure Note

Infrastructure must be implemented using an Infrastructure as Code approach, because IaC is a mandatory project requirement.