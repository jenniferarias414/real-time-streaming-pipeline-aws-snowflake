# Cleanup Checklist

Cloud resources can incur cost. Clean up lab resources after screenshots and repo files are saved.

## AWS Cleanup

- [ ] Delete API Gateway REST API.
- [ ] Delete Lambda function.
- [ ] Delete Kinesis Data Stream.
- [ ] Delete Firehose delivery stream.
- [ ] Empty S3 data bucket.
- [ ] Delete S3 data bucket.
- [ ] Empty S3 error bucket.
- [ ] Delete S3 error bucket.
- [ ] Delete Snowpipe IAM role if it was only used for this lab.
- [ ] Delete Lambda/API/Kinesis IAM role if it was only used for this lab.
- [ ] Remove broad permissions created for the lab.
- [ ] Review CloudWatch log groups and delete lab-only log groups if desired.

## Snowflake Cleanup

- [ ] Drop pipe if no longer needed.
- [ ] Drop stage if no longer needed.
- [ ] Drop storage integration if no longer needed.
- [ ] Drop raw table/database if no longer needed.
- [ ] Suspend warehouse.

Example SQL:

```sql
USE ROLE ACCOUNTADMIN;
DROP PIPE IF EXISTS REALTIME_STREAMING_DB.RAW.STREAMING_EVENTS_PIPE;
DROP STAGE IF EXISTS REALTIME_STREAMING_DB.RAW.S3_RAW_STAGE;
DROP TABLE IF EXISTS REALTIME_STREAMING_DB.RAW.STREAMING_EVENTS_RAW;
DROP DATABASE IF EXISTS REALTIME_STREAMING_DB;
DROP STORAGE INTEGRATION IF EXISTS S3_REALTIME_INT;
ALTER WAREHOUSE COMPUTE_WH SUSPEND;
```
