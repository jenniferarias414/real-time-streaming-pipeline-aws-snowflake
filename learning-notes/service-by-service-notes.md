# Service-by-Service Notes

This file explains each service in the pipeline in plain language, connected back to the project.

## Postman

Postman is the test client. It sends HTTP POST requests to API Gateway. In a real system, this could be a web app, mobile app, backend service, vendor feed, or event producer.

## Amazon API Gateway

API Gateway is the front door. It exposes an HTTPS endpoint so outside clients can send data into AWS.

In this project, API Gateway receives JSON events from Postman and invokes Lambda through a proxy integration.

## AWS Lambda

Lambda is the validation and routing layer. It runs Python code without needing a server.

In this project, Lambda:

- reads the API Gateway request body
- parses the JSON
- checks whether `Id` is present and not blank
- sends valid records to Kinesis
- sends invalid records to the S3 error bucket

Lambda is useful here because it gives us a place to add custom logic before the data reaches the streaming layer.

## Amazon Kinesis Data Streams

Kinesis Data Streams captures valid events as a real-time stream.

In this project, Lambda writes valid records to Kinesis. The stream acts as the handoff between validation and delivery. If another downstream consumer needed the same data later, it could also read from the stream.

## Amazon Data Firehose

Firehose delivers streaming data to a destination.

In this project, Firehose reads from Kinesis and writes JSON files to the S3 data bucket. Firehose also buffers records, which means files may not appear instantly. That is normal.

## Amazon S3

S3 is the storage layer.

This project uses two buckets:

- a data bucket for valid raw JSON files
- an error bucket for invalid records

The data bucket has a `raw/` prefix. The error bucket has an `errors/` prefix.

## AWS IAM

IAM controls permissions.

This project required IAM because services need permission to talk to each other. For example:

- Lambda needs permission to write to Kinesis and S3.
- Firehose needs permission to write files into S3.
- Snowflake needs permission to read from the S3 raw location.

For a learning lab, broad managed policies were used to move quickly. In production, these permissions should be narrowed to least privilege.

## CloudWatch Logs

CloudWatch stores Lambda logs.

This became useful during troubleshooting. When Postman returned an error, the Lambda logs helped identify the issue. This is a realistic debugging pattern: check the service logs closest to the failing step.

## Snowflake External Stage

The external stage points Snowflake to the S3 raw folder.

It does not copy the data by itself. It tells Snowflake where the files are and how to access them.

## Snowpipe

Snowpipe loads new files from S3 into Snowflake automatically.

In this project, Snowpipe uses an S3 event notification. When a new file lands in the raw prefix, S3 sends a notification to Snowflake's queue, and Snowpipe loads the file into the raw table.

## Snowflake Raw Table

The raw table stores the JSON event as `VARIANT`.

This is a good first landing pattern for semi-structured data because it preserves the original event. Later models can flatten the JSON into typed columns for reporting and analytics.
