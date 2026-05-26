# Screenshot Checklist

Use these screenshot names so the README and case study can stay organized.

## AWS Setup

- `02-iam-role-created.png`
- `02-iam-role-policies.png`
- `03-s3-buckets-created.png`
- `04-s3-data-raw-folder.png`
- `05-s3-error-folder.png`
- `06-kinesis-data-stream-created.png`
- `07-firehose-delivery-stream-created.png`

## Lambda

- `08-lambda-function-created.png`
- `09-lambda-environment-variables.png`
- `10-lambda-code-deployed.png`
- `11-lambda-test-valid-event.png`
- `12-lambda-test-invalid-event.png`
- `13-s3-error-output-from-lambda.png`
- `14-s3-valid-output-from-firehose.png`

## API Gateway + Postman

- `15-api-gateway-created.png`
- `16-api-gateway-lambda-integration.png`
- `17-api-gateway-deployed-stage.png`
- `18-api-gateway-invoke-url.png` optional
- `19-postman-valid-request.png`
- `20-postman-invalid-request.png`
- `21-s3-valid-output-after-api-gateway.png`
- `22-s3-error-output-after-api-gateway.png`

## Snowflake / Snowpipe

- `23-snowpipe-iam-role-created.png`
- `24-snowflake-database-schema-created.png`
- `25-snowflake-storage-integration-created.png`
- `26-snowpipe-role-trust-policy-updated.png`
- `27-snowflake-stage-list-success.png`
- `28-snowflake-raw-table-created.png`
- `29-snowpipe-created-notification-channel.png`
- `30-s3-event-notification-for-snowpipe.png`
- `31-postman-valid-request-after-snowpipe.png`
- `32-s3-raw-file-after-snowpipe-test.png`
- `33-snowflake-query-loaded-data.png`

## Notes

Some screenshot numbers may be skipped depending on what was captured during the lab. That is okay. The important evidence is:

1. AWS resources exist.
2. Lambda can route valid and invalid events.
3. API Gateway/Postman can trigger the pipeline externally.
4. Valid data reaches S3 and Snowflake.
5. Invalid data reaches the S3 error bucket.
