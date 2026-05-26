# Project Explanation Guide

This is a natural way to explain the project without overcomplicating it.

## 30-second version

I built a guided real-time streaming pipeline using AWS and Snowflake. The project simulates an external application sending JSON events through API Gateway. Lambda validates each event, sends valid records to Kinesis, Firehose writes them to S3, and Snowpipe loads the files into Snowflake. If a record has a blank or missing `Id`, Lambda routes it to an S3 error bucket instead of sending it through the main pipeline.

## Slightly deeper version

The goal was to understand how a real-time ingestion architecture works across multiple cloud services. I used Postman to simulate an API client sending JSON events. API Gateway exposed the HTTP endpoint and invoked Lambda. Lambda handled validation and routing. Valid events went to Kinesis Data Streams and were delivered to the S3 raw bucket by Firehose. Snowpipe then auto-ingested the S3 files into a Snowflake raw table using a Snowflake stage and storage integration.

I also tested the error path by sending an invalid event with a blank `Id`. That record was written to the S3 error bucket, which showed how a pipeline can separate bad records without stopping valid ingestion.

## What I personally built and tested

- IAM role and permissions for the project services
- S3 data and error buckets
- Kinesis Data Stream
- Firehose delivery stream to S3
- Lambda validation/routing function
- API Gateway REST endpoint
- Postman valid and invalid API tests
- Snowflake database/schema/raw table
- Snowflake storage integration, external stage, and Snowpipe
- End-to-end query proving the event loaded into Snowflake

## Why these services were used

- API Gateway gives outside clients a secure HTTP entry point.
- Lambda adds custom validation and routing logic.
- Kinesis handles real-time streaming events.
- Firehose reliably delivers the stream into S3.
- S3 stores durable raw files and invalid records.
- Snowpipe automates ingestion from S3 into Snowflake.
- CloudWatch helps troubleshoot Lambda and pipeline errors.
- IAM controls service-to-service access.

## Questions I can answer from this project

### Why put Lambda between API Gateway and Kinesis?

Lambda gives us a place to validate, transform, enrich, or reject data before it enters the stream. In this project, Lambda checks the `Id` field and sends invalid records to an error bucket.

### Why use Firehose?

Firehose makes it easy to deliver streaming data into S3 without building a custom consumer. It handles buffering and delivery, which is useful for data lake landing zones.

### Why use Snowpipe?

Snowpipe lets Snowflake automatically ingest new files from S3. Instead of manually running a load command every time a file arrives, Snowpipe responds to S3 event notifications and loads data into the raw table.

### How did you handle errors?

The Lambda function has validation logic. If the event is missing a valid `Id`, it writes the record to an S3 error bucket. That keeps invalid records out of the main stream while preserving them for review.

### How did you know the pipeline worked?

I tested it in layers. First, I tested Lambda directly. Then I tested the AWS path with Postman through API Gateway and confirmed output in S3. Finally, after Snowpipe was configured, I sent a valid event and queried the Snowflake raw table to confirm the record loaded successfully.

## Honest project context

This was a guided data engineering project completed as part of my studies. The value for me was not just following the steps, but understanding how the services connect and documenting the project in a way I can explain later.
