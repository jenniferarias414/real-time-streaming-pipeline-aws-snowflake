# Screenshots

This folder contains screenshots collected during the build.

The current repo starter includes the screenshots available at packaging time. Additional screenshots can be added later using the names in `docs/screenshot-checklist.md`.

Recommended next additions if available locally:

- `18-api-gateway-invoke-url.png` optional
- `20-postman-invalid-request.png`
- `21-s3-valid-output-after-api-gateway.png`
- `22-s3-error-output-after-api-gateway.png`
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

The strongest proof screenshot currently included is:

- `33-snowflake-query-loaded-data.png`

That screenshot shows the event successfully loaded into Snowflake, which proves end-to-end success.


## Optional final screenshot

`33-snowflake-query-loaded-data.png` already proves end-to-end success because it shows the Postman event loaded into Snowflake. If a separate final proof image is desired later, save a wider version as `34-end-to-end-success.png`.
