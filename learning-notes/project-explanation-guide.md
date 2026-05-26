# Project Explanation Guide

This is how I would explain the project out loud without turning it into a giant AWS vocabulary quiz.

## Quick version

I built a guided real-time streaming pipeline with AWS and Snowflake.

Postman sends JSON events to API Gateway. API Gateway calls Lambda. Lambda validates the event. If the event is valid, Lambda sends it to Kinesis, Firehose writes it to S3, and Snowpipe loads it into Snowflake. If the event is missing a valid `Id`, Lambda sends it to an S3 error bucket instead.

## Slightly deeper version

The goal was to understand how real-time ingestion works across several cloud services.

I used Postman as the test client. API Gateway exposed the endpoint. Lambda handled validation and routing. Kinesis acted as the streaming layer. Firehose delivered valid records to S3. Snowpipe watched the S3 raw folder and loaded new files into Snowflake.

I also tested the error path by sending a record with a blank `Id`. That record skipped the main stream and landed in the S3 error bucket. That showed how the pipeline can separate bad records without stopping good records from loading.

## What I built and tested

- IAM role and permissions for AWS service access
- S3 data and error buckets
- Kinesis Data Stream
- Firehose delivery stream to S3
- Lambda validation/routing function
- API Gateway REST endpoint
- Postman valid and invalid request tests
- Snowflake database, schema, and raw table
- Snowflake storage integration, external stage, and Snowpipe
- Final Snowflake query proving the event loaded

## Why the services are there

- **API Gateway**: gives the pipeline an HTTPS entry point.
- **Lambda**: validates the event and decides where it should go.
- **Kinesis**: receives valid events as a stream.
- **Firehose**: delivers the stream to S3.
- **S3**: stores raw valid events and invalid error records.
- **Snowpipe**: loads new S3 files into Snowflake automatically.
- **CloudWatch**: helps troubleshoot Lambda/API issues.
- **IAM**: controls which service is allowed to access which resource.

## Questions this project helped me answer

### Why put Lambda between API Gateway and Kinesis?

Because Lambda gives me a checkpoint before the data enters the stream. I can validate the payload, reject bad records, add fields, transform data, or route different records to different places.

### Why use Firehose?

Firehose saves me from writing my own custom consumer just to move data from Kinesis into S3. It handles buffering and delivery.

### Why use Snowpipe?

Snowpipe loads files from S3 into Snowflake automatically. I do not have to manually run a copy command every time a new file lands.

### How did I handle bad data?

The Lambda function checks the `Id` field. If it is blank or missing, the event goes to the S3 error bucket. That keeps the main pipeline cleaner and preserves the bad record for review.

### How did I know it worked?

I tested it in layers:

1. Lambda test events.
2. Postman through API Gateway.
3. S3 raw and error bucket outputs.
4. Snowflake query showing the loaded record.

That final Snowflake query is the proof that the event traveled through the full pipeline.

## Project context

This was a guided project from my data engineering studies. I kept the repo polished enough to show the completed build, but I also kept these notes because the real value was understanding how all the services connect.
