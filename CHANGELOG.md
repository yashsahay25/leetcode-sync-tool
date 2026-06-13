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

## 2026-06-13

- Added a scheduled GitHub Actions workflow for syncing LeetCode submissions automatically.
- Added manual workflow dispatch support so syncs can be triggered from the GitHub Actions tab.
- Configured the workflow to run daily at 12:30 AM IST.
- Configured Python setup and dependency installation in GitHub Actions.
- Configured LeetCode credentials to be read from GitHub Actions secrets: `LEETCODE_SESSION` and `CSRF_TOKEN`.
- Fixed `requirements.txt` so it only lists installable Python package dependencies.
