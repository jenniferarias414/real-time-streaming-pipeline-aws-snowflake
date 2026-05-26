# Learning Notes

These are Jenny's notes for the real-time streaming project.

The main `README.md` is the clean, recruiter-friendly overview. This folder is the slower walkthrough: what I built, why each piece exists, what confused me at first, and what I want future-me to remember when I come back to this later.

The goal is not to sound fancy. The goal is to make the project make sense.

## What's in this folder

- `end-to-end-walkthrough.md` — the full pipeline from Postman to Snowflake.
- `service-by-service-notes.md` — what each AWS/Snowflake service did in this project.
- `s3-iam-study-notes.md` — S3 and IAM concepts that showed up while building the lab.
- `operations-and-error-handling.md` — logs, errors, buffering, and reprocessing notes.
- `project-explanation-guide.md` — a natural way to explain the project out loud.

## Why these notes exist

A lot of this project was not "write code and run it." It was more like connecting a bunch of cloud services and making sure every handoff worked:

```text
API Gateway has to call Lambda.
Lambda has to write to Kinesis and S3.
Firehose has to deliver to S3.
Snowflake has to read from S3.
Snowpipe has to notice when new files arrive.
```

That is easy to forget if all I keep is a polished README. These notes keep the messy-but-useful explanation close to the project.

## Tone of these notes

These are not meant to be formal product docs. They are working notes: plain language first, technical terms where they actually help, and enough context that someone learning cloud data engineering could follow the story without already knowing every AWS service by heart.

They say "drinking from a firehose," but that's an understatement when you're building multiple projects with brand-new tools while your job keeps throwing new stories at you. So yes — these README.md files are absolutely necessary. I might forget what I ate for lunch by the end of the day, if you're picking up what I'm putting down.
