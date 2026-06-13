# Architecture

This document explains how `leetcode-sync-tool` works at a high level, how data moves through the system, and how the scheduled GitHub Actions workflow writes submissions into the archive repository.

## Repository Model

`leetcode-sync-tool` and `leetcode-submissions-archive` intentionally have separate responsibilities.

```mermaid
flowchart LR
    A["leetcode-sync-tool"] -->|"contains Python sync engine"| B["GitHub Actions runner"]
    B -->|"fetches accepted submissions"| C["LeetCode GraphQL API"]
    B -->|"writes files and commits"| D["leetcode-submissions-archive"]

    A -."stores workflow and code".-> A
    D -."stores solution files and Git history".-> D
```

The sync-tool repository stores automation code. The archive repository stores the generated submission files and their timestamped commit history.

## Scheduled Workflow

The GitHub Actions workflow runs from `leetcode-sync-tool`, but the archive repository is checked out separately and used as the working directory for generated files.

```mermaid
flowchart TD
    A["Scheduled or manual workflow starts"] --> B["Checkout leetcode-sync-tool into sync-tool/"]
    B --> C["Checkout leetcode-submissions-archive into archive/"]
    C --> D["Set up Python"]
    D --> E["Install dependencies from sync-tool/requirements.txt"]
    E --> F["Configure Git author inside archive/"]
    F --> G["Run python -m archiver.main"]
    G --> H["Create commits inside archive/"]
    H --> I["Push archive commits to leetcode-submissions-archive"]
```

The workflow sets `PYTHONPATH` to the sync-tool checkout, then runs the package from inside `archive/`. Because the current working directory is the archive checkout, generated files and Git commits are created in `leetcode-submissions-archive`.

## Runtime Flow

The Python package starts at `archiver/main.py`, then delegates to `run_archiver()`.

```mermaid
sequenceDiagram
    participant Main as archiver/main.py
    participant Orchestrator as archiver/archiver.py
    participant API as archiver/leetcode_api.py
    participant Client as archiver/graphql_client.py
    participant LeetCode as LeetCode GraphQL API
    participant Git as archiver/git_manager.py
    participant Archive as Archive checkout

    Main->>Orchestrator: run_archiver()
    Orchestrator->>Orchestrator: validate_auth_config()
    Orchestrator->>API: fetch_all_questions()
    API->>Client: safe_post(userProgressQuestionList)
    Client->>LeetCode: POST /graphql
    LeetCode-->>Client: solved questions
    Client-->>API: parsed response
    API-->>Orchestrator: questions

    loop For each solved question
        Orchestrator->>API: fetch_accepted_submissions(slug)
        API->>Client: safe_post(userProgressSubmissionList)
        Client->>LeetCode: POST /graphql
        LeetCode-->>Client: submissions
        API-->>Orchestrator: accepted submissions sorted by timestamp

        loop For each accepted submission
            Orchestrator->>Archive: check filename exists
            alt File already exists
                Orchestrator->>Orchestrator: skip submission
            else New submission
                Orchestrator->>API: fetch_submission_code(submission_id)
                API->>Client: safe_post(submissionDetails)
                Client->>LeetCode: POST /graphql
                LeetCode-->>Client: source code
                API-->>Orchestrator: code
                Orchestrator->>Archive: write source file
                Orchestrator->>Git: commit_file(file, message, timestamp)
                Git->>Archive: git add + git commit with original timestamp
            end
        end
    end
```

## Package Components

```mermaid
flowchart TD
    A["archiver/main.py"] --> B["archiver/archiver.py"]
    B --> C["archiver/leetcode_api.py"]
    C --> D["archiver/graphql_client.py"]
    D --> E["LeetCode GraphQL API"]
    B --> F["archiver/git_manager.py"]
    B --> G["archiver/config.py"]
    C --> G
    D --> G
    B --> H["archiver/logger.py"]
    C --> H
    D --> H
    F --> H
```

| Component | Responsibility |
| --- | --- |
| `archiver/main.py` | Package entrypoint for `python -m archiver.main`. |
| `archiver/archiver.py` | Coordinates the full sync process. |
| `archiver/leetcode_api.py` | Defines LeetCode GraphQL operations and pagination. |
| `archiver/graphql_client.py` | Sends authenticated GraphQL requests with retry/backoff handling. |
| `archiver/git_manager.py` | Creates timestamped Git commits for new submission files. |
| `archiver/config.py` | Reads credentials and stores throttling/retry configuration. |
| `archiver/logger.py` | Prints timestamped progress logs. |

## Idempotency Model

Every accepted submission is keyed by its LeetCode submission ID.

```mermaid
flowchart TD
    A["Accepted submission"] --> B["Build filename: <problemId>_<slug>_<submissionId>.cpp"]
    B --> C{"Does file already exist in archive checkout?"}
    C -->|"Yes"| D["Skip"]
    C -->|"No"| E["Fetch source code"]
    E --> F["Write file"]
    F --> G["Commit file with original submission timestamp"]
```

Because `submissionId` is included in the filename, multiple accepted submissions for the same problem can coexist. Already archived submissions are skipped on later runs because their files are already present in the archive checkout.

## Authentication And Permissions

```mermaid
flowchart LR
    A["LEETCODE_SESSION"] --> C["LeetCode authenticated GraphQL requests"]
    B["CSRF_TOKEN"] --> C
    D["ARCHIVE_REPO_TOKEN"] --> E["Checkout and push leetcode-submissions-archive"]
```

Required secrets live in the `leetcode-sync-tool` repository:

```text
LEETCODE_SESSION
CSRF_TOKEN
ARCHIVE_REPO_TOKEN
```

`LEETCODE_SESSION` and `CSRF_TOKEN` authenticate LeetCode requests. `ARCHIVE_REPO_TOKEN` gives the workflow write access to `leetcode-submissions-archive`.

## Failure And Retry Behavior

GraphQL calls are wrapped by `safe_post()`, which retries transient failures with exponential backoff and random jitter.

```mermaid
flowchart TD
    A["Send GraphQL request"] --> B{"HTTP 200 and no GraphQL errors?"}
    B -->|"Yes"| C["Return response data"]
    B -->|"No"| D{"Retries remaining?"}
    D -->|"Yes"| E["Sleep with exponential backoff + jitter"]
    E --> A
    D -->|"No"| F["Raise max retries exceeded"]
```

The sync also uses human-like delays between LeetCode requests and longer cooling breaks after a configured number of questions.
