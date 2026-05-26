# End-to-End Walkthrough

## The short version

This project simulates an application sending JSON events into a cloud data pipeline. Valid records are streamed into AWS, stored in S3, and loaded into Snowflake. Invalid records are separated into an S3 error bucket so they can be reviewed instead of breaking the main pipeline.

```text
Postman
→ API Gateway
→ Lambda
→ Kinesis Data Streams
→ Firehose
→ S3 raw bucket
→ Snowpipe
→ Snowflake raw table
```

Error path:

```text
Postman
→ API Gateway
→ Lambda
→ S3 error bucket
```

## Why Postman is part of the project

Postman is not part of the production pipeline. It is the test client. In this lab, Postman pretends to be an external application sending events through an HTTP POST request.

This matters because it proves the pipeline can receive data from outside AWS, not just from an internal Lambda test event.

The Postman/API Gateway test proved that the AWS side of the pipeline worked before Snowflake was added:

```text
Postman sent JSON
→ API Gateway accepted the HTTP request
→ Lambda parsed and validated the payload
→ valid records moved into Kinesis
→ Firehose delivered records into S3
→ invalid records were routed to the S3 error bucket
```

Once Snowpipe was added, a final valid event proved the full end-to-end path into Snowflake.

## Valid record path

A valid event has a non-blank `Id` field. For this lab, the validation rule is intentionally simple.

Example valid payload:

```json
{
  "Id": "3001",
  "customer_id": "C300",
  "event_type": "purchase",
  "amount": 199.99,
  "payment_type": "card",
  "event_time": "2026-05-26T12:00:00Z"
}
```

What happens next:

1. API Gateway receives the HTTP POST request.
2. API Gateway invokes the Lambda function.
3. Lambda parses the request body into JSON.
4. Lambda checks the `Id` field.
5. If `Id` is valid, Lambda writes the record to Kinesis.
6. Firehose reads from Kinesis and writes the event into the S3 `raw/` prefix.
7. Snowpipe watches for new files in S3 and loads them into the Snowflake raw table.
8. The row becomes queryable in Snowflake.

## Invalid record path

An invalid event has a blank or missing `Id`.

Example invalid payload:

```json
{
  "Id": "",
  "customer_id": "C301",
  "event_type": "purchase",
  "amount": 49.99,
  "payment_type": "card",
  "event_time": "2026-05-26T12:05:00Z"
}
```

What happens next:

1. API Gateway receives the request.
2. Lambda parses the JSON.
3. Lambda identifies that `Id` is blank.
4. Instead of sending the bad record to Kinesis, Lambda writes it to the S3 error bucket under `errors/`.

That pattern is common in data engineering: keep the main pipeline moving, but preserve bad records so they can be reviewed and reprocessed later.

## What Snowflake stores

The Snowflake raw table stores the JSON payload in a `VARIANT` column. This is useful because raw JSON may not always be perfectly flat or predictable.

A raw table is usually the first landing table. Later, the data can be transformed into cleaner models with typed columns, business rules, and reporting-friendly structure.

## What I learned from building this

The biggest learning point was how many small configuration details have to line up:

- Lambda needs permission to write to Kinesis and S3.
- Firehose needs permission to write to the S3 data bucket.
- API Gateway needs permission to invoke Lambda.
- Snowflake needs an AWS IAM role and external ID trust relationship.
- S3 event notifications need to point to the Snowpipe notification channel.

The code is not the whole project. A lot of the work is wiring cloud services together securely and testing each step before moving on.
