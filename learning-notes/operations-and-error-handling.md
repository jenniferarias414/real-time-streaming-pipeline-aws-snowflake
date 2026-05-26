# Operations and Error Handling Notes

This project is not only about moving data. It also shows operational thinking: how to monitor, troubleshoot, and handle bad records.

## Monitoring

The first place to check is CloudWatch Logs. Lambda writes execution logs there automatically.

When Postman returned a `502 Bad Gateway`, the useful question was not “Is Postman broken?” The better troubleshooting path was:

```text
Postman reached API Gateway
→ API Gateway tried to invoke Lambda
→ check Lambda logs in CloudWatch
→ find the syntax/runtime error
→ fix Lambda code
→ deploy again
→ retest Postman
```

That is a realistic cloud debugging workflow.

## Error routing

The Lambda function uses simple validation. If `Id` is blank or missing, the record is routed to S3 instead of Kinesis.

Why this is useful:

- Bad records do not break the valid data pipeline.
- Invalid data is not lost.
- The team can inspect the error bucket later.
- Bad records can be corrected and reprocessed if needed.

## Reprocessing idea

This lab does not automate reprocessing, but a realistic process would be:

1. Inspect the record in the S3 error bucket.
2. Identify why it failed validation.
3. Fix the payload or fix the Lambda validation logic if the rule was too strict.
4. Re-submit the corrected record through API Gateway/Postman or another replay process.

## Firehose buffering

Firehose may not write to S3 immediately. That is expected.

Firehose buffers records before writing them to S3. Buffering helps reduce tiny file problems, lower S3 request overhead, and improve delivery efficiency. In this lab, the buffer settings were made small so files appeared quickly while testing.

Plain English:

```text
Kinesis receives the event quickly.
Firehose may wait a little before writing the file to S3.
That delay does not automatically mean the pipeline is broken.
```

## What I would improve in a production version

A production version could add:

- stricter JSON schema validation
- dead-letter queue or replay workflow
- CloudWatch alarms for Lambda errors
- SNS/email alerts for failures
- least-privilege IAM policies
- Terraform infrastructure code
- Snowflake transformed views or dbt models
- monitoring for Snowpipe load history

## Key lesson

The pipeline is more than the happy path. A good data pipeline also needs logging, error handling, and a way to reason through where a failure happened.
