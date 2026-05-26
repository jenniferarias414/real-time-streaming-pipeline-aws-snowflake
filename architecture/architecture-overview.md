# Architecture Overview

## High-Level Flow

```text
Postman / external client
→ API Gateway
→ Lambda
→ Kinesis Data Streams
→ Firehose
→ S3 raw bucket
→ Snowpipe
→ Snowflake raw table
```

Invalid records are routed to a separate S3 error bucket:

```text
API Gateway → Lambda → S3 error bucket
```

## Component Responsibilities

### Postman / Client

Postman simulates an application sending real-time JSON events through an HTTP POST request.

### API Gateway

API Gateway provides the public API endpoint. It receives the HTTP request and forwards it to Lambda.

### Lambda

Lambda validates and routes the incoming data.

- Valid event: has a non-blank `Id`
- Invalid event: missing or blank `Id`

Valid records go to Kinesis. Invalid records go to S3 error storage.

### Kinesis Data Streams

Kinesis receives valid records from Lambda and holds them as a stream of events.

### Firehose

Firehose reads events from Kinesis and writes them to S3 as JSON files. This creates the raw landing zone for Snowflake.

### S3 Raw Bucket

The raw bucket stores valid JSON files under the `raw/` prefix.

### S3 Error Bucket

The error bucket stores invalid records under the `errors/` prefix.

### Snowflake External Stage

The external stage points Snowflake to the S3 raw folder.

### Snowpipe

Snowpipe automatically loads new S3 files into Snowflake when S3 object-created notifications are received.

### Snowflake Raw Table

The raw table stores JSON records in a `VARIANT` column so the original event can be preserved before future transformations.
