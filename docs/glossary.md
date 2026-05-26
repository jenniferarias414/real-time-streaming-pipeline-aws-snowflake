# Glossary

## API Gateway
A managed AWS service for creating APIs. In this project, it receives HTTP POST requests from Postman.

## Lambda
Serverless compute. In this project, Lambda validates the JSON payload and routes it to Kinesis or the error bucket.

## Kinesis Data Streams
A real-time streaming service. It stores event records temporarily so other services can consume them.

## Firehose
A delivery service that writes streaming data to destinations like S3. In this project, it delivers Kinesis records to the S3 raw bucket.

## S3 Bucket
Object storage in AWS. This project uses one bucket for valid raw data and another for error records.

## Raw Folder / Prefix
A logical S3 path where untransformed valid JSON files land.

## Error Folder / Prefix
A logical S3 path where invalid records are stored for review.

## Snowflake
A cloud data warehouse. In this project, Snowflake stores and queries the streamed event data.

## External Stage
A Snowflake object that points to files stored outside Snowflake, such as in S3.

## Snowpipe
A Snowflake service that automatically loads files from a stage into a table.

## VARIANT
A Snowflake data type for semi-structured data such as JSON.

## IAM Role
An AWS identity with permissions. Roles allow services like Lambda, Firehose, and Snowflake to access AWS resources.

## Least Privilege
A security principle where a role only gets the permissions it needs and nothing extra.
