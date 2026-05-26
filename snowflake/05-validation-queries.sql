USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE REALTIME_STREAMING_DB;
USE SCHEMA RAW;

-- Optional: refresh the pipe if you need Snowpipe to scan files that already existed before auto-ingest was configured.
-- ALTER PIPE STREAMING_EVENTS_PIPE REFRESH;

SELECT *
FROM STREAMING_EVENTS_RAW
ORDER BY LOAD_TIMESTAMP DESC;

-- Example fields from the VARIANT column.
SELECT
    DATA:Id::STRING AS id,
    DATA:customer_id::STRING AS customer_id,
    DATA:event_type::STRING AS event_type,
    DATA:amount::NUMBER(10,2) AS amount,
    DATA:payment_type::STRING AS payment_type,
    DATA:event_time::STRING AS event_time,
    LOAD_TIMESTAMP
FROM STREAMING_EVENTS_RAW
ORDER BY LOAD_TIMESTAMP DESC;
