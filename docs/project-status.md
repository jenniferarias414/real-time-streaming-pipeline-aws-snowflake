# Project Status

## Completed So Far

- Created IAM role for project services.
- Attached broad managed policies for the learning lab.
- Created S3 data and error buckets.
- Created `raw/` prefix in the data bucket.
- Created `errors/` prefix in the error bucket.
- Created Kinesis Data Stream.
- Created Firehose delivery stream with S3 destination.
- Created Lambda function.
- Added Lambda environment variables.
- Deployed Lambda validation/routing code.
- Tested Lambda with valid event.
- Tested Lambda with invalid event.
- Confirmed invalid record in S3 error bucket.
- Confirmed valid record delivered by Firehose to S3 raw bucket.
- Created API Gateway REST API.
- Integrated API Gateway with Lambda using proxy integration.
- Deployed API Gateway to `dev` stage.
- Tested valid event from Postman.
- Confirmed AWS pipeline worked before Snowflake.
- Created Snowflake database/schema/raw table.
- Created Snowflake storage integration, stage, and Snowpipe.
- Configured S3 event notification for Snowpipe.
- Confirmed event loaded into Snowflake.

## Remaining / Optional

- Add screenshots for any missing Snowflake setup steps.
- Add more sample events.
- Add typed Snowflake views that flatten the `DATA` variant column.
- Add Terraform version of the architecture.
- Add cleanup screenshots.
- Add portfolio case study page.
- Add OneNote recap and interview script.
