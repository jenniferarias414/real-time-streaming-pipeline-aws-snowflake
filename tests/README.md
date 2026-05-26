# Tests

Automated tests are planned for a future improvement.

This project was validated manually through:
- Lambda test events
- Postman API Gateway requests
- S3 output verification
- Snowflake query validation

Future tests could include:
- Unit tests for Lambda validation logic
- Mocked boto3 tests for Kinesis and S3 routing
- JSON schema validation tests
- Integration test documentation for the API Gateway → Lambda → Kinesis → Firehose → S3 flow