# Design Decisions

## Why API Gateway?

API Gateway creates a managed HTTP endpoint for incoming events. This lets external tools or applications send JSON data into AWS without directly calling Lambda.

## Why Lambda?

Lambda is used for lightweight validation and routing. It keeps the project serverless and simple.

## Why Kinesis Data Streams?

Kinesis Data Streams represents the real-time streaming layer. Lambda sends valid events to the stream, allowing downstream services to consume records as they arrive.

## Why Firehose?

Firehose simplifies delivery from Kinesis to S3. Instead of writing custom consumer code, Firehose buffers records and writes files to the S3 raw bucket.

## Why S3?

S3 is the durable raw landing zone. It keeps a historical copy of incoming events and gives Snowflake a stable place to load from.

## Why a separate error bucket?

Bad records should not stop the main pipeline. Sending invalid records to a separate error bucket preserves them for review while keeping the valid data flow clean.

## Why Snowpipe?

Snowpipe automates the loading of new S3 files into Snowflake. This avoids manual `COPY INTO` commands for each file.

## Why store raw JSON as VARIANT?

The raw table is meant to preserve the original event. Snowflake `VARIANT` supports semi-structured JSON, which is useful before creating more structured silver/gold tables.

## Production Improvements

This lab uses broad IAM policies for speed. A production version should use least-privilege IAM policies, stronger schema validation, encryption requirements, monitoring alarms, retries, dead-letter queues, and infrastructure as code.
