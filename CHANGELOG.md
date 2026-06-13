# Changelog

All notable changes to `leetcode-sync-tool` are tracked here.

When changes are made directly on the `main` branch, add them under the appropriate date block. Multiple changes on the same day should stay grouped under that date.

## 2026-06-14

- Renamed the project documentation from `leetcode-archiver` to `leetcode-sync-tool`.
- Updated documentation to distinguish the sync tool repository from the storage repository.
- Updated the GitHub Actions workflow to checkout `yashsahay25/leetcode-submissions-archive` as the target archive repository.
- Changed the workflow so submissions are written and committed from the archive checkout instead of the sync-tool checkout.
- Added the `ARCHIVE_REPO_TOKEN` setup requirement for cross-repository pushes.
- Added this changelog and established date-grouped tracking for future `main` branch changes.
- Expanded the changelog with the earlier February 2026 project setup and hardening changes.
- Added `docs/ARCHITECTURE.md` with high-level architecture, scheduled workflow, runtime flow, package component, idempotency, authentication, and retry diagrams.
- Linked the architecture documentation from `README.md` and updated the project structure listing.

## 2026-06-13

- Added a scheduled GitHub Actions workflow for syncing LeetCode submissions automatically.
- Added manual workflow dispatch support so syncs can be triggered from the GitHub Actions tab.
- Configured the workflow to run daily at 12:30 AM IST.
- Configured Python setup and dependency installation in GitHub Actions.
- Configured LeetCode credentials to be read from GitHub Actions secrets: `LEETCODE_SESSION` and `CSRF_TOKEN`.
- Fixed `requirements.txt` so it only lists installable Python package dependencies.

## 2026-02-22

- Added the initial production-ready LeetCode sync package under `archiver/`.
- Added `archiver/main.py` as the package entrypoint.
- Added `archiver/archiver.py` to orchestrate solved-question lookup, accepted-submission lookup, source-code download, file writing, and timestamped commits.
- Added `archiver/leetcode_api.py` with LeetCode GraphQL calls for solved questions, per-problem submission history, and full submission code retrieval.
- Added `archiver/graphql_client.py` with a persistent `requests.Session`, retry handling, exponential backoff, jitter, timeout handling, and GraphQL error detection.
- Added `archiver/git_manager.py` to commit each archived submission with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to the original LeetCode submission timestamp.
- Added `archiver/config.py` for GraphQL endpoint, auth headers, throttling, retry, and cooling configuration.
- Added `archiver/logger.py` for timestamped console logging.
- Added idempotent filename behavior using `<problemId>_<slug>_<submissionId>.cpp`, allowing multiple accepted submissions for the same problem while skipping already archived submissions.
- Added the initial README documenting architecture, flow, LeetCode GraphQL APIs, rate limiting, retries, idempotency, run instructions, and future improvements.
- Changed LeetCode credentials from hardcoded placeholders to `LEETCODE_SESSION` and `CSRF_TOKEN` environment variables.
- Added auth validation so runs fail fast when LeetCode credentials are missing.
- Updated README auth setup instructions to use exported environment variables instead of editing source files.
- Removed an old suggested repository-description note from the README.
- Added `alfa-leetcode-api` to the README references.
