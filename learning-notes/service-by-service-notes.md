# Service-by-Service Notes

This is the same project, broken down one service at a time.

## Postman

Postman is the pretend app.

It sends a JSON request to the API endpoint so I can test the pipeline without building a whole frontend or backend application.

In a real system, Postman could be replaced by a web app, mobile app, vendor system, payment API, or another internal service.

## Amazon API Gateway

API Gateway is the front door.

It gives the outside world an HTTPS endpoint. In this project, Postman sends a `POST` request to API Gateway, and API Gateway passes that request to Lambda.

The important part: API Gateway is how data enters AWS from the outside.

## AWS Lambda

Lambda is the checkpoint.

It runs the Python logic that decides what to do with each event.

In this project, Lambda:

- reads the API Gateway request body
- parses the JSON
- checks whether `Id` exists and is not blank
- sends valid records to Kinesis
- sends invalid records to the S3 error bucket

Lambda is useful here because it gives the pipeline a place to validate, clean up, enrich, or reject data before it enters the stream.

## Amazon Kinesis Data Streams

Kinesis Data Streams is the real-time stream.

Once Lambda decides a record is valid, it writes the event to Kinesis. Kinesis acts like the handoff point between validation and downstream delivery.

A useful way to think about it: Kinesis is not the final storage location. It is the moving stream of events.

## Amazon Data Firehose

Firehose is the delivery truck.

It reads from Kinesis and writes the records into S3 as JSON files.

Firehose also buffers records, which means files may not appear in S3 instantly. That delay is normal. Firehose is trying to write data efficiently instead of creating a million tiny files.

## Amazon S3

S3 is the landing zone.

This project uses two buckets:

- data bucket: valid JSON files under `raw/`
- error bucket: invalid JSON files under `errors/`

The data bucket feeds Snowflake. The error bucket is for troubleshooting and possible reprocessing.

## AWS IAM

IAM is the permission system.

Nothing in this project works unless the services are allowed to talk to each other.

Examples:

- Lambda needs permission to write to Kinesis.
- Lambda needs permission to write to the error bucket.
- Firehose needs permission to write to the data bucket.
- Snowflake needs permission to read from the S3 raw path.

For the lab, I used broad managed policies to move faster. In a production version, I would scope those permissions down to least privilege.

## CloudWatch Logs

CloudWatch is where I looked when things broke.

When Postman returned an error, the fix was not to stare at Postman forever. The useful move was to check Lambda logs in CloudWatch, find the syntax/runtime issue, fix the code, deploy again, and retest.

That felt very real-world.

## Snowflake External Stage

The external stage tells Snowflake where the S3 files live.

It does not load the data by itself. It is more like Snowflake saying, "Here is the S3 folder I am allowed to read from."

## Snowpipe

Snowpipe is the automatic loader.

When a new file lands in the S3 `raw/` folder, an event notification lets Snowpipe know there is something new to load. Snowpipe then runs the load into the Snowflake raw table.

This is what makes the S3-to-Snowflake part feel close to real time.

## Snowflake raw table

The raw table is the first Snowflake landing table.

It stores the JSON event in a `VARIANT` column. That keeps the original event shape available before any flattening, cleanup, or business logic happens later.
