# Postman Sample Requests

## Valid Event Request

Method:

```text
POST
```

URL format:

```text
https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/dev/events
```

Headers:

```text
Content-Type: application/json
```

Body:

```json
{
  "Id": "3001",
  "customer_id": "C300",
  "event_type": "purchase",
  "amount": 199.99,
  "payment_type": "card",
  "event_time": "2026-05-26T12:00:00Z"
}
```

Expected response:

```json
{
  "message": "Valid JSON sent to Kinesis stream",
  "stream_name": "dea-realtime-streaming-stream",
  "partition_key": "3001"
}
```

## Invalid Event Request

Body:

```json
{
  "Id": "",
  "customer_id": "C301",
  "event_type": "purchase",
  "amount": 49.99,
  "payment_type": "card",
  "event_time": "2026-05-26T12:05:00Z"
}
```

Expected response:

```json
{
  "message": "Invalid JSON routed to S3 error bucket"
}
```

## Why This Test Matters

The Postman test proves an external client can call the API and trigger the AWS side of the pipeline. It is different from the Lambda console test because it validates the API Gateway integration too.
