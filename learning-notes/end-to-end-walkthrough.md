# End-to-End Walkthrough

## The short version

This project simulates an app sending JSON events into a cloud data pipeline.

Valid records go through the main pipeline:

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

Bad records take a separate path:

```text
Postman
→ API Gateway
→ Lambda
→ S3 error bucket
```

The point is simple: keep good data moving, but do not throw away bad data.

## What Postman is doing here

Postman is not part of the production pipeline. It is just pretending to be an app or outside system sending data to us.

In real life, this could be a website, mobile app, vendor feed, payment system, airline system, or any backend service that sends events through an API.

For this lab, Postman gave me a safe way to send test JSON into API Gateway and prove the AWS side worked before Snowflake was added.

That first Postman test proved this part:

```text
Postman sent JSON
→ API Gateway accepted the request
→ Lambda parsed and validated it
→ valid data went to Kinesis
→ Firehose delivered it to S3
→ invalid data went to the S3 error bucket
```

Then Snowpipe was added so the valid files in S3 could load into Snowflake automatically.

## The valid data path

A valid event has a non-blank `Id` field.

Example:

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

What happens:

1. Postman sends the JSON as an HTTP POST request.
2. API Gateway receives the request.
3. API Gateway invokes Lambda.
4. Lambda reads the request body and parses it as JSON.
5. Lambda checks the `Id` field.
6. If the `Id` is good, Lambda sends the event to Kinesis.
7. Firehose reads from Kinesis and writes the event to S3 under `raw/`.
8. Snowpipe sees the new S3 file and loads it into the Snowflake raw table.
9. The event becomes queryable in Snowflake.

## The invalid data path

An invalid event has a blank or missing `Id`.

Example:

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

What happens:

1. API Gateway still receives the request.
2. Lambda still parses the JSON.
3. Lambda sees that `Id` is blank.
4. Instead of putting it into the main stream, Lambda writes it to the S3 error bucket under `errors/`.

That error bucket matters. It means the bad record is not lost, but it also does not contaminate the main data path.

## What Snowflake stores

The Snowflake raw table stores the event in a `VARIANT` column.

That means Snowflake keeps the JSON mostly as-is instead of forcing it into separate columns right away.

This makes sense for a raw layer because raw event data can change over time. Later, the JSON could be flattened into typed columns for reporting or analytics.

## The biggest thing I learned

The code was only one part of the project.

The harder part was getting all the services to trust each other and pass data correctly:

- API Gateway needed permission to invoke Lambda.
- Lambda needed permission to write to Kinesis and S3.
- Firehose needed permission to write files to the S3 data bucket.
- Snowflake needed an IAM role and external ID trust relationship to read from S3.
- S3 needed an event notification so Snowpipe could react to new files.

This is a big part of cloud data engineering: the pipeline is not just code. It is code plus permissions, configuration, storage paths, event notifications, and testing each handoff.
