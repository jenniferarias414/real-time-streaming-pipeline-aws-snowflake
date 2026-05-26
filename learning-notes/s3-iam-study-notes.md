# S3 and IAM Study Notes

These notes connect the course S3/IAM exercises back to this project.

## S3 versioning

Versioning means S3 can keep multiple versions of the same object instead of overwriting the old one completely.

Why it matters:

- It can protect against accidental overwrite or deletion.
- It helps with recovery because older versions can still exist.
- It is required for some replication setups.

How to enable it in the console:

1. Open the S3 bucket.
2. Go to **Properties**.
3. Find **Bucket Versioning**.
4. Click **Edit**.
5. Choose **Enable** and save.

Versioning is not the same as backup by itself, but it is a useful protection feature.

## S3 cross-region replication

Cross-region replication copies objects from one S3 bucket in one AWS region to another S3 bucket in another region.

Why a company might use it:

- disaster recovery
- regional outage protection
- compliance requirements
- keeping data closer to users in another region

Important detail: versioning must be enabled on both buckets for replication.

This project did not fully build cross-region replication, but the concept connects to data durability and disaster recovery. In a more production-ready version of this project, the raw S3 landing bucket could be replicated to another region for extra resilience.

## IAM: what the policy is really saying

IAM policies are JSON documents that answer three main questions:

```text
Who/what gets access?
What actions can it perform?
Which resources can it perform those actions on?
```

Example read-only S3 object access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadAccess",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::*/*"
    }
  ]
}
```

This allows reading objects from any bucket. That is useful for an exercise, but it is broad. In production, it would usually be scoped to specific buckets or prefixes.

## Least privilege

Least privilege means giving a service only the permissions it needs and nothing extra.

For this learning lab, broad AWS managed policies made setup faster. A production version would narrow permissions like this:

- Lambda can write only to the specific Kinesis stream.
- Lambda can write only to the specific error bucket/prefix.
- Firehose can write only to the specific raw bucket/prefix.
- Snowflake can read only from the specific raw S3 location.

## Common IAM mistake: ARN formatting

A lot of IAM errors come from tiny ARN mistakes.

Example pattern for Kinesis stream ARNs:

```text
arn:aws:kinesis:region:account-id:stream/stream-name
```

If the ARN is malformed, the policy may not apply to the intended resource, even if the action looks correct.

## How this connects to the project

This project worked only because IAM permissions lined up correctly:

- API Gateway could invoke Lambda.
- Lambda could write valid events to Kinesis.
- Lambda could write invalid events to S3.
- Firehose could write S3 files.
- Snowflake could assume an AWS IAM role and read the raw S3 location.

That is a huge part of cloud data engineering: not just writing code, but wiring services together with the right permissions.
