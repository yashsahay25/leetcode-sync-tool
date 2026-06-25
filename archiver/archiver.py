import os
import time
from .leetcode_api import (
    fetch_all_questions,
    fetch_accepted_submissions,
    fetch_submission_code,
    validate_leetcode_session
)
from .git_manager import commit_file
from .config import COOLING_INTERVAL, COOLING_DURATION, validate_auth_config
from .logger import log


def run_archiver():
    log("===== STARTING LEETCODE ARCHIVER =====")
    validate_auth_config()
    validate_leetcode_session()   # add import from leetcode_api

    questions = fetch_all_questions()

    if not questions:
        raise RuntimeError(
            "Authentication failed or no solved questions found. "
            "Please update LEETCODE_SESSION and CSRF_TOKEN."
        )
    
    total = len(questions)

    for idx, q in enumerate(questions, start=1):
        slug = q["titleSlug"]
        frontend_id = q["frontendId"]

        log(f"\n----- [{idx}/{total}] Processing: {frontend_id} {slug} -----")

        accepted = fetch_accepted_submissions(slug)

        for sub in accepted:
            submission_id = sub["id"]
            timestamp = sub["timestamp"]

            filename = f"{int(frontend_id):05d}_{slug}_{submission_id}.cpp"

            if os.path.exists(filename):
                log(f"Skipping existing: {filename}")
                continue

            code = fetch_submission_code(submission_id)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            commit_file(filename, f"{frontend_id} {slug}", timestamp)

        if idx % COOLING_INTERVAL == 0:
            log(f"Cooling for {COOLING_DURATION}s...")
            time.sleep(COOLING_DURATION)

    log("===== ARCHIVE COMPLETE =====")
