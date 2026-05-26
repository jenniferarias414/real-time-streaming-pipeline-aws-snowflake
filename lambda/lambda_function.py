"""
AWS Lambda function for the Real-Time Streaming Pipeline project.

Purpose:
- Receive JSON from API Gateway.
- Validate that the payload has a usable Id value.
- Send valid events to Amazon Kinesis Data Streams.
- Route invalid events to an S3 error bucket.

This is intentionally small and readable because the goal of the lab is to understand
how the AWS services connect, not to build a production validation framework.
"""

import json
import os
from datetime import datetime, timezone

import boto3


# These are configured in Lambda environment variables instead of hardcoded.
# That makes the function easier to reuse across environments.
KINESIS_STREAM_NAME = os.environ["KINESIS_STREAM_NAME"]
ERROR_BUCKET_NAME = os.environ["ERROR_BUCKET_NAME"]
ERROR_PREFIX = os.environ.get("ERROR_PREFIX", "errors/")

s3_client = boto3.client("s3")
kinesis_client = boto3.client("kinesis")


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    API Gateway sends the HTTP request body to Lambda as a string.
    Lambda converts the string into JSON, checks the Id field, then routes the record.
    """
    try:
        body = event.get("body", "{}")

        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        event_id = data.get("Id")

        # For this lab, a blank or missing Id means the record is invalid.
        if event_id is None or event_id == "":
            error_key = build_error_key()

            s3_client.put_object(
                Bucket=ERROR_BUCKET_NAME,
                Key=error_key,
                Body=json.dumps(data),
                ContentType="application/json",
            )

            return build_response(
                200,
                {
                    "message": "Invalid JSON routed to S3 error bucket",
                    "error_bucket": ERROR_BUCKET_NAME,
                    "error_key": error_key,
                },
            )

        # Valid records are sent to Kinesis.
        # Firehose reads from Kinesis and writes the data into the S3 raw folder.
        # The newline helps keep Firehose output friendly for JSON loading.
        kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=json.dumps(data) + "\n",
            PartitionKey=str(event_id),
        )

        return build_response(
            200,
            {
                "message": "Valid JSON sent to Kinesis stream",
                "stream_name": KINESIS_STREAM_NAME,
                "partition_key": str(event_id),
            },
        )

    except Exception as error:
        print(f"Error processing event: {error}")

        return build_response(
            500,
            {
                "message": "Error processing event",
                "error": str(error),
            },
        )


def build_error_key():
    """Create a unique S3 key for invalid records."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    return f"{ERROR_PREFIX}error_{timestamp}.json"


def build_response(status_code, body):
    """Return a standard API Gateway-friendly response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
