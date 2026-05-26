# Operations and Error Handling Notes

This project was not just about moving data from point A to point B. It also had the more realistic part: what happens when something goes wrong?

## Monitoring

The first place I checked was CloudWatch Logs.

When Postman returned a `502 Bad Gateway`, the issue was not really Postman. Postman had reached the API. Something behind the API was failing.

The better troubleshooting path was:

```text
Postman sent request
→ API Gateway tried to call Lambda
→ Lambda hit an error
→ CloudWatch logs showed the issue
→ fix Lambda code
→ deploy again
→ retest
```

That is a useful habit: follow the path of the data and check the logs closest to the failure.

## Error routing

The Lambda function checks the `Id` field.

If `Id` is good, the record goes to Kinesis.

If `Id` is blank or missing, the record goes to the S3 error bucket.

Why I like this pattern:

- Good records keep moving.
- Bad records are not lost.
- The main stream does not get polluted with known-bad data.
- Someone can inspect the error bucket later and decide what to do.

## Reprocessing idea

This project does not fully automate reprocessing, but the idea is clear.

A realistic process could be:

1. Open the failed record in the S3 error bucket.
2. Figure out why it failed.
3. Fix the payload or fix the validation rule.
4. Send the corrected event back through the API.

That could be manual at first, then automated later.

## Firehose buffering

Firehose does not always write to S3 immediately.

That is not automatically a bug.

Firehose buffers records so it can write files more efficiently. Bigger batches usually mean fewer tiny files and fewer S3 writes.

For this lab, the buffer settings were small so files showed up faster while testing.

Plain English version:

```text
Kinesis receives the event quickly.
Firehose may wait a short time before writing to S3.
A small delay is normal.
```

## What I would improve later

A more production-ready version could add:

- stricter JSON schema validation
- dead-letter queue or replay process
- CloudWatch alarms
- SNS/email alerts
- least-privilege IAM policies
- Terraform for repeatable infrastructure
- dbt or SQL models to flatten the raw JSON
- Snowpipe load history monitoring

## Key lesson

A pipeline is not done just because the happy path works.

A better question is:

```text
Can I tell where it failed?
Did I preserve the bad data?
Can I replay or fix the failed record later?
```

That is the operations side of data engineering.
