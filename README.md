# 🟢 leetcode-archiver

A production-grade LeetCode historical submission archiver that syncs all accepted submissions to GitHub while preserving original submission timestamps.

---

## 📌 Table of Contents

1. Overview  
2. Features  
3. Architecture 
4. Project Structure 
4. High-Level Flow  
5. GraphQL APIs Used  
6. Rate Limiting & Throttling Strategy  
7. Retry & Backoff Strategy  
8. Idempotency Design  
9. How to Run  
10. Design Decisions  
11. References  

---

## 1️⃣ Overview

`leetcode-archiver` is a Python-based automation tool that:

- Fetches all solved problems from LeetCode
- Retrieves all accepted submissions (`status = 10`)
- Downloads source code
- Commits each submission to GitHub
- Preserves original submission timestamps

This provides a complete historical archive of your LeetCode journey.

---

## 2️⃣ Features

- Historical sync of all accepted submissions  
- Preserves original submission timestamps  
- Safe throttling and rate limiting  
- Exponential backoff retry logic  
- Network error handling  
- Resume-safe (idempotent) execution  
- Modular architecture  
- Chronological Git history  

---

## 3️⃣ Architecture

```
main.py
   ↓
archiver.py
   ↓
leetcode_api.py
   ↓
graphql_client.py
   ↓
LeetCode GraphQL API
```

Git handling is abstracted in:

```
git_manager.py
```

Logging handled by:

```
logger.py
```

---

## 📁 Project Structure

```
leetcode-archiver/
│
├── archiver/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── graphql_client.py
│   ├── leetcode_api.py
│   ├── git_manager.py
│   └── archiver.py
│
├── main.py
├── requirements.txt
└── README.md
```

### File Responsibilities

- `main.py` → Entry point  
- `archiver.py` → Orchestrates full archive process  
- `leetcode_api.py` → Handles LeetCode GraphQL queries  
- `graphql_client.py` → Manages retries, throttling, backoff  
- `git_manager.py` → Handles timestamped commits  
- `config.py` → Stores configuration & throttling settings  
- `logger.py` → Structured timestamp logging  

## 4️⃣ High-Level Flow Diagram

```
┌──────────────────────────────┐
│ Fetch Solved Questions       │
└──────────────┬───────────────┘
               ↓
┌───────────────────────────────────────┐
│ For each question:                    │
│   Fetch all submissions               │
│   Filter status == 10 (Accepted)      │
└──────────────┬────────────────────────┘
               ↓
┌───────────────────────────────────────┐
│ For each accepted submission:         │
│   Fetch submission code               │
│   Write file                          │
│   Commit with original timestamp      │
└──────────────┬────────────────────────┘
               ↓
┌───────────────────────────────────────┐
│ Cooling break every N questions       │
└───────────────────────────────────────┘
```

---

## 5️⃣ LeetCode GraphQL APIs Used

### 1️⃣ userProgressQuestionList

Used to fetch all solved problems.

```graphql
query userProgressQuestionList($filters: UserProgressQuestionListInput)
```

---

### 2️⃣ userProgressSubmissionList

Used to fetch submission history per problem.

```graphql
query userProgressSubmissionList($offset: Int!, $limit: Int!, $questionSlug: String!)
```

---

### 3️⃣ submissionDetails

Used to fetch full source code.

```graphql
query submissionDetails($submissionId: Int!)
```

---

## 6️⃣ Rate Limiting & Throttling Strategy

To avoid blacklisting:

- Sequential requests only (no parallelization)
- 1–2 second randomized delay per request
- Cooling break every N questions
- Persistent HTTP session (requests.Session)
- Authenticated GraphQL calls only
- No scraping or unofficial endpoints

This mimics normal human browsing behavior.

---

## 7️⃣ Retry & Backoff Strategy

Implemented:

- Maximum 10 retries per request
- Exponential backoff
- Random jitter added
- Network exception handling
- Handles:
  - 429 (Too Many Requests)
  - 400 errors
  - SSL errors
  - Connection resets
  - Timeouts

Backoff formula:

```
(2^attempt) + random(2–4 seconds)
```

This prevents aggressive retry bursts.

---

## 8️⃣ Idempotency Design

The tool is resume-safe.

Before writing a file:

```python
if os.path.exists(filename):
    skip
```

This ensures:

- No duplicate commits
- Safe restarts after crash
- Safe incremental execution

Each file name includes submission ID:

```
<problemId>_<slug>_<submissionId>.cpp
```

This guarantees uniqueness and prevents overwrites.

---

## 9️⃣ How to Run

### 1. Clone repository

```
git clone https://github.com/<your-username>/leetcode-archiver.git
cd leetcode-archiver
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Export auth tokens

Set environment variables before running:

```bash
export LEETCODE_SESSION="<your_session_cookie>"
export CSRF_TOKEN="<your_csrf_token>"
```

### 4. Run

```
python main.py
```

---

## 🔟 Design Decisions

### Why sequential over parallel?

LeetCode rate limits are undocumented.  
Sequential execution with jitter is safer and more stable.

---

### Why exponential backoff?

Prevents hammering the API during instability and network issues.

---

### Why commit per submission?

Preserves chronological evolution and exact historical timeline.

---

### Why include submission ID in filename?

Ensures idempotency and prevents accidental overwrites.

---

## 11️⃣ References

- glsync: https://github.com/ahmed-e-abdulaziz/glsync  
- LeetCode Progress Page: https://leetcode.com/progress/  
- LeetCode GraphQL endpoint: https://leetcode.com/graphql  

---

## 🚀 Future Improvements

- Incremental sync mode  
- CLI flags (`--full-sync`, `--incremental`)  
- Topic-based folder structure  
- Progress persistence file  
- Docker support  
- GitHub Actions automation  

---

## 🏁 Final Note

This project demonstrates:

- API reverse engineering  
- Rate-limit-aware design  
- Idempotent architecture  
- Exponential backoff retry systems  
- Clean modular backend structure  

Built with engineering discipline.
