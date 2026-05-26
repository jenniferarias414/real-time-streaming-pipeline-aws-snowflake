# GitHub Push Steps

The GitHub repo has already been created as:

```text
real-time-streaming-pipeline-aws-snowflake
```

From the project folder:

```bash
git init
git add .
git commit -m "Initial real-time streaming pipeline project"
git branch -M main
git remote add origin https://github.com/jenniferarias414/real-time-streaming-pipeline-aws-snowflake.git
git push -u origin main
```

If the repo already has a remote or existing commit history:

```bash
git remote -v
git status
git add .
git commit -m "Add AWS and Snowflake streaming pipeline documentation"
git push
```

## Important

`notes/private/` is intentionally gitignored. It can stay local for personal learning notes, but it will not be pushed to GitHub.
