import time
import random
from .graphql_client import safe_post
from .config import DELAY_MIN, DELAY_MAX
from .logger import log


def human_delay():
    sleep_time = random.uniform(DELAY_MIN, DELAY_MAX)
    log(f"Sleeping {sleep_time:.2f}s")
    time.sleep(sleep_time)

def validate_leetcode_session():
    """Verify the session is still signed in before starting the sync."""
    
    payload = {
        "query": """
        query {
          userStatus {
            isSignedIn
            username
          }
        }
        """
    }
    
    data = safe_post(payload, "Validate Session")
    status = data.get("data", {}).get("userStatus")
    
    if not status or not status.get("isSignedIn"):
        raise RuntimeError(
            "LeetCode session is not signed in. "
            "Refresh LEETCODE_SESSION and CSRF_TOKEN in GitHub secrets."
        )
    
    log(f"Authenticated as: {status.get('username')}")
    
def fetch_all_questions():
    questions = []
    skip = 0
    limit = 50

    while True:
        payload = {
            "query": """
            query userProgressQuestionList($filters: UserProgressQuestionListInput) {
              userProgressQuestionList(filters: $filters) {
                questions {
                  titleSlug
                  frontendId
                }
              }
            }
            """,
            "variables": {
                "filters": {"skip": skip, "limit": limit}
            }
        }

        data = safe_post(payload, "Fetch Questions")
        batch = data["data"]["userProgressQuestionList"]["questions"]

        if not batch:
            break

        questions.extend(batch)
        skip += limit
        human_delay()

    log(f"Total Questions: {len(questions)}")
    return questions


def fetch_accepted_submissions(slug):
    submissions = []
    offset = 0
    limit = 20

    while True:
        payload = {
            "query": """
            query userProgressSubmissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
              userProgressSubmissionList(
                offset: $offset
                limit: $limit
                questionSlug: $questionSlug
              ) {
                submissions {
                  id
                  status
                  timestamp
                }
                totalNum
              }
            }
            """,
            "variables": {
                "offset": offset,
                "limit": limit,
                "questionSlug": slug
            }
        }

        data = safe_post(payload, f"Fetch Submissions: {slug}")
        result = data["data"]["userProgressSubmissionList"]

        for sub in result["submissions"]:
            if sub["status"] == 10:
                submissions.append(sub)

        offset += limit
        if offset >= result["totalNum"]:
            break

        human_delay()

    submissions.sort(key=lambda x: int(x["timestamp"]))
    return submissions


def fetch_submission_code(submission_id):
    payload = {
        "query": """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
          }
        }
        """,
        "variables": {
            "submissionId": int(submission_id)
        }
    }

    data = safe_post(payload, f"Fetch Code: {submission_id}")
    human_delay()

    return data["data"]["submissionDetails"]["code"]
