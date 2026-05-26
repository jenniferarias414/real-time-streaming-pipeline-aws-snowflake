-- Replace the role ARN and S3 path before running.
-- This allows Snowflake to assume an AWS IAM role and read files from S3.

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;

CREATE OR REPLACE STORAGE INTEGRATION S3_REALTIME_INT
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'PASTE_YOUR_SNOWPIPE_ROLE_ARN_HERE'
  STORAGE_ALLOWED_LOCATIONS = ('s3://dea-realtime-streaming-data-jenny/raw/');

-- Copy STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID from this output.
-- Then paste those values into the AWS IAM role trust policy.
DESC INTEGRATION S3_REALTIME_INT;
