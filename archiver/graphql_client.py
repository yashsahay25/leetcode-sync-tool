import requests
import time
import random
from requests.exceptions import RequestException
from .config import GRAPHQL_URL, HEADERS, MAX_RETRIES
from .logger import log

session = requests.Session()
session.headers.update(HEADERS)

def safe_post(payload, description="GraphQL Call"):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log(f"→ {description} (Attempt {attempt}/{MAX_RETRIES})")

            response = session.post(
                GRAPHQL_URL,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    log(f"⚠ GraphQL Error: {data['errors']}")
                    raise Exception("GraphQL error")
                return data

            backoff = (2 ** attempt) + random.uniform(2.0, 4.0)

            log(f"[{response.status_code}] HTTP error. Sleeping {backoff:.2f}s")
            time.sleep(backoff)

        except RequestException as e:
            backoff = (2 ** attempt) + random.uniform(3.0, 6.0)
            log(f"⚠ Network error: {str(e)}")
            log(f"Sleeping {backoff:.2f}s before retry")
            time.sleep(backoff)

    raise Exception("Max retries exceeded")