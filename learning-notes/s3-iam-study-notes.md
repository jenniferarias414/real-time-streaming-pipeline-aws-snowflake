# S3 and IAM Study Notes

These notes connect the course S3/IAM exercises back to the project I actually built.

## S3 versioning

Versioning means S3 can keep older copies of an object instead of fully replacing the old one when a file with the same name is uploaded.

Why that matters:

- It can help recover from accidental overwrite.
- It can help recover from accidental delete.
- It is required for some replication setups.

Basic console path:

```text
S3 bucket → Properties → Bucket Versioning → Edit → Enable
```

One thing to remember: versioning is helpful, but it is not magic. It can also increase storage usage because old versions stay around unless lifecycle rules clean them up.

## S3 cross-region replication

Cross-region replication means objects from one S3 bucket are copied to another bucket in a different AWS region.

Why a company might care:

- disaster recovery
- regional outage protection
- compliance requirements
- keeping a backup copy somewhere else

Important detail: versioning needs to be enabled on both buckets.

This project did not build cross-region replication, but the idea fits the project. A production version could replicate the raw landing bucket to another region so the event archive is more resilient.

## IAM policies: the short version

IAM policies are JSON permission rules.

They basically answer:

```text
What actions are allowed?
Which resources are those actions allowed on?
Is this allowed or denied?
```

Example idea:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-bucket/*"
}
```

That says: allow reading objects from that bucket.

## Least privilege

Least privilege means giving a service only what it needs, not every permission under the sun.

For the lab, broad AWS managed policies helped keep the project moving. That is fine for learning, but not ideal for production.

A production version would be tighter:

- Lambda can write only to the one Kinesis stream it needs.
- Lambda can write only to the one error bucket/prefix.
- Firehose can write only to the one raw bucket/prefix.
- Snowflake can read only from the one S3 raw path.

## ARN formatting matters

ARNs are picky.

A tiny typo in an ARN can make a policy fail even when the idea is right.

Kinesis stream ARN pattern:

```text
arn:aws:kinesis:region:account-id:stream/stream-name
```

That `stream/stream-name` part matters.

## How IAM showed up in this project

This project worked because the permissions lined up:

- API Gateway could invoke Lambda.
- Lambda could write to Kinesis.
- Lambda could write bad records to S3.
- Firehose could write valid records to S3.
- Snowflake could assume an AWS role and read from S3.

That is a real cloud lesson: sometimes the project is not failing because the code is wrong. Sometimes one service simply does not have permission to talk to the next service.
