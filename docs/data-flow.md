# Data Flow

## Overview

This document describes the planned data flow for the project.

## Flow Steps

### 1. Bronze Layer - Raw Ingestion

- Hacker News data is collected on a daily basis.
- X data is imported from an existing dataset.
- Raw data is stored in Amazon S3 in its original format.
- No transformation is allowed in this stage.

### 2. Silver Layer - Data Normalization

Raw bronze-layer data is transformed into a consistent and queryable structure.

Normalization includes:
- flattening nested structures
- aligning timestamps into a single UTC format
- cleaning values such as HTML tags
- removing duplicates
- defining a normalized schema
- storing datasets in parquet format with partitioning

### 3. Gold Layer - Metrics and KPIs

Silver-layer data is used to generate business metrics and KPI datasets.

Examples include:
- daily number of Hacker News posts by type
- daily number of users on both platforms
- top X users by follower count
- top Hacker News users by karma score
- top Hacker News job offers by score
- top Hacker News stories by score

### 4. Serving Layer

Gold-layer datasets are loaded from S3 into PostgreSQL.

This step is required because Apache Superset will use PostgreSQL as the data source for dashboards and visualizations.

## Summary

The complete logical flow is:

**Hacker News / X dataset -> Bronze S3 -> Silver parquet datasets -> Gold metrics -> PostgreSQL -> Apache Superset**