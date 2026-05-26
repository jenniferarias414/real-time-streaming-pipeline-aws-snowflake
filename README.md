# Real-Time Streaming Pipeline with AWS and Snowflake

## Overview

This project builds an end-to-end real-time streaming pipeline using AWS and Snowflake.

The pipeline simulates an external application sending JSON events through an API. Valid events are streamed through AWS services, stored in Amazon S3, and automatically loaded into Snowflake through Snowpipe. Invalid events are routed to a separate S3 error bucket for review.

```text
Postman / API Client
→ Amazon API Gateway
→ AWS Lambda validation
<the file was replaced with the updated README contents>
- Postman valid request
- S3 raw output
- S3 error output
- Snowflake query result showing loaded data

## Current Status

Completed:

- AWS budget/cost awareness step reviewed
- IAM role created
- S3 data and error buckets created
- Kinesis Data Stream created
- Firehose delivery stream created
- Lambda validation and routing created
- Lambda valid and invalid tests passed
- API Gateway created and deployed
- Postman valid request succeeded
- S3 raw output confirmed
- S3 error output confirmed
- Snowflake/Snowpipe setup completed
- Snowflake query confirmed end-to-end success

Remaining / optional improvements:

- Add more formal Snowflake transformed views
- Add Terraform version of the infrastructure
- Add CI/CD deployment notes
- Add CloudWatch metric screenshots
- Add cost cleanup screenshots after resources are deleted

## Security Notes

This is a learning lab. Some AWS managed policies used here are intentionally broad to move quickly through the bootcamp project.

For production, permissions should be restricted to least privilege. For example, Lambda should only access the specific Kinesis stream and S3 buckets it needs, and Snowflake should only read from the exact S3 path used for ingestion.

## Cleanup

This project uses cloud resources that can incur cost. After testing, clean up unused resources:

- API Gateway
- Lambda function
- Kinesis Data Stream
- Firehose delivery stream
- S3 objects and buckets
- IAM roles/policies created only for the lab
- Snowflake pipe/stage/table/database if no longer needed
- Snowflake warehouse if it is running

See `docs/cleanup-checklist.md` for a more detailed cleanup list.

## What I Learned

This project helped connect several important data engineering concepts:

- API-based ingestion
- Serverless validation
- Streaming data movement
- Error routing / quarantine patterns
- Raw S3 landing zones
- Snowflake external stages
- Snowpipe auto-ingestion
- Querying semi-structured JSON data in Snowflake

The biggest learning outcome was seeing how each service has a specific job in the pipeline, and how testing each section separately makes troubleshooting much easier.
