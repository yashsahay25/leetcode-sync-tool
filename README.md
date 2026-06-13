# leetcode-sync-tool

A Python-based sync tool that fetches accepted LeetCode submissions and commits them to a separate archive repository while preserving the original submission timestamps.

This repository contains the sync/automation code. The submission store is intended to live in:

```text
yashsahay25/leetcode-submissions-archive
```

## Overview

`leetcode-sync-tool` is responsible for:

- Fetching solved problems from LeetCode
- Retrieving accepted submissions (`status = 10`) for each problem
- Downloading the submitted source code
- Writing each submission as a uniquely named file
- Creating Git commits using the original LeetCode submission timestamp
- Skipping submissions that already exist in the target archive checkout

The target archive repository stores the actual solution files and chronological commit history.

## Repository Roles

```text
yashsahay25/leetcode-sync-tool
```

Contains the Python sync engine, LeetCode API client, throttling/retry logic, and GitHub Actions automation.

```text
yashsahay25/leetcode-submissions-archive
```

Contains the archived LeetCode submission files and the historical commit timeline.

## Features

- Historical sync of accepted submissions
- Supports multiple accepted submissions for the same problem
- Preserves original submission timestamps in Git history
- Resume-safe execution using submission IDs in filenames
- Sequential, rate-limit-aware LeetCode API access
- Retry logic with exponential backoff and jitter
- Manual and scheduled GitHub Actions workflow support

## Architecture

```text
archiver/main.py
   -> archiver/archiver.py
   -> archiver/leetcode_api.py
   -> archiver/graphql_client.py
   -> LeetCode GraphQL API
```

Git commit handling lives in:

```text
archiver/git_manager.py
```

Configuration and credentials are read from:

```text
archiver/config.py
```

## Project Structure

```text
leetcode-sync-tool/
  archiver/
    archiver.py
    config.py
    git_manager.py
    graphql_client.py
    leetcode_api.py
    logger.py
    main.py
  .github/
    workflows/
      leetcode-sync.yml
  requirements.txt
  README.md
```

## Idempotency

Each accepted submission is written with the LeetCode submission ID in the filename:

```text
<problemId>_<slug>_<submissionId>.cpp
```

Before writing a file, the sync checks whether that filename already exists:

```python
if os.path.exists(filename):
    skip
```

That means previously archived submissions are skipped on later runs. Multiple accepted submissions for the same question are preserved because each submission has a unique submission ID.

## Local Run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set LeetCode credentials:

```bash
export LEETCODE_SESSION="<your_session_cookie>"
export CSRF_TOKEN="<your_csrf_token>"
```

Run the sync entrypoint:

```bash
python -m archiver.main
```

## GitHub Actions

The scheduled workflow is defined at:

```text
.github/workflows/leetcode-sync.yml
```

It currently runs daily at `12:30 AM IST` and can also be triggered manually from the Actions tab.

Required repository secrets:

```text
LEETCODE_SESSION
CSRF_TOKEN
```

The workflow should be updated to checkout and push into `yashsahay25/leetcode-submissions-archive` as the target archive repository.

## Notes

LeetCode session cookies can expire. If the scheduled workflow starts failing with authentication errors, refresh `LEETCODE_SESSION` and `CSRF_TOKEN` in GitHub Actions secrets.
