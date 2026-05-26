# Troubleshooting Notes

## Postman returns 502 Bad Gateway

A 502 response usually means API Gateway reached Lambda, but Lambda failed or returned an invalid response.

Check:

1. Lambda code syntax.
2. Lambda environment variables.
3. CloudWatch logs for the Lambda function.
4. API Gateway Lambda proxy integration is enabled.
5. API Gateway was redeployed after changes.

## Lambda test succeeds but Postman fails

Check:

1. API Gateway integration points to the correct Lambda function.
2. API Gateway has permission to invoke Lambda.
3. The deployed stage is current.
4. The Postman URL includes the correct stage/path, such as `/dev/events`.

## Valid Postman event does not appear in S3 immediately

Firehose buffers records before writing to S3. Wait 30-90 seconds and refresh the S3 `raw/` folder.

## Invalid event does not appear in the error bucket

Check:

1. `ERROR_BUCKET_NAME` Lambda environment variable.
2. `ERROR_PREFIX` Lambda environment variable.
3. Lambda IAM role has S3 write permissions.
4. CloudWatch logs for Lambda errors.

## Snowflake stage cannot list S3 files

Check:

1. Storage integration role ARN.
2. AWS IAM trust policy uses the Snowflake IAM user ARN and external ID.
3. S3 allowed location matches the real bucket and prefix.
4. The S3 path ends with `/raw/` if that is where Firehose writes files.

## Snowpipe does not load new files

Check:

1. `SHOW PIPES;` notification channel was copied correctly.
2. S3 event notification points to the Snowflake SQS ARN.
3. S3 event notification prefix is `raw/`.
4. New files were created after the pipe and event notification were configured.
5. Try `ALTER PIPE STREAMING_EVENTS_PIPE REFRESH;` for files that already existed.
