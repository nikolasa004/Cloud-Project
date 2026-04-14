# Manual AWS Setup Notes

This document records the manual AWS configuration used during the initial development and testing phase of the project.

The purpose of this file is to preserve the infrastructure decisions before they are later translated into Infrastructure as Code (IaC).

---

## 1. S3 Bucket

### Bucket name
`ftn-social-data-pipeline-2026`

### Bucket type
- General purpose bucket

### Region
- Europe (Frankfurt) `eu-central-1`

### Bucket configuration
- Object Ownership: ACLs disabled / Bucket owner enforced
- Block all public access: Enabled
- Bucket versioning: Disabled
- Tags: None
- Default encryption: Default AWS-managed encryption
- Object Lock: Disabled

### Data lake folder / prefix layout
The bucket is used as the main data lake bucket for the project.

Created prefixes:
- `bronze/`
- `bronze/hackernews/`
- `bronze/x/`
- `silver/`
- `gold/`

---

## 2. IAM Role for Bronze Hacker News Lambda

### Role name
`bronze-hackernews-lambda-role`

### Trusted entity type
- AWS service

### Use case
- Lambda

### Attached managed policy
- `AWSLambdaBasicExecutionRole`

This policy is used so the Lambda function can write logs to CloudWatch.

### Inline S3 write policy
Policy name:
`BronzeHackerNewsS3WritePolicy`

Policy document:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowWriteBronzeHackerNews",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::ftn-social-data-pipeline-2026/bronze/hackernews/*"
    }
  ]
}
```

This policy allows the Lambda function to upload raw Hacker News bronze-layer files into the correct S3 prefix.

## 3. Lambda Function for Bronze Hacker News

### Function name
`bronze-hackernews-ingestion`

### Runtime
- Python

### Architecture
- x86_64

### Execution role
- Use existing role
- Selected role: `bronze-hackernews-lambda-role`

### Environment variables
- `BUCKET_NAME=ftn-social-data-pipeline-2026`

### General configuration
- Timeout: 2 minutes
- Memory: 512 MB

### Runtime settings
Handler:
`src.bronze.hackernews.handler.lambda_handler`

### Deployment package notes
The Lambda deployment package currently contains:
- the Hacker News bronze handler
- the Hacker News bronze collector
- required Python dependencies such as `requests`

The package was uploaded manually during the initial testing phase.

---

## 4. Bronze Hacker News Behavior

The Bronze Hacker News Lambda is designed to:
- collect Hacker News data for the previous UTC day
- keep the data in raw/original form
- upload the collected JSON payload to the S3 bronze layer

### Target S3 key format
`bronze/hackernews/date=YYYY-MM-DD/hn_bronze_YYYY-MM-DD.json`

---

## 5. Why these notes exist

This manual setup is temporary.

Later, all of the following should be moved to IaC:
- S3 bucket definition
- IAM role and policies
- Lambda function
- environment variables
- resource configuration

These notes are kept so the same infrastructure can be recreated through IaC without guessing the original manual setup.