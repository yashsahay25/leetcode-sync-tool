import os

GRAPHQL_URL = "https://leetcode.com/graphql"

# Prefer environment variables over hardcoding secrets.
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION", "")
CSRF_TOKEN = os.getenv("CSRF_TOKEN", "")

HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRF_TOKEN}",
    "x-csrftoken": CSRF_TOKEN,
    "Referer": "https://leetcode.com",
}

# 🛑 Throttling Config
DELAY_MIN = 1.0
DELAY_MAX = 4.0
MAX_RETRIES = 10

# 🧊 Cooling strategy
COOLING_INTERVAL = 25
COOLING_DURATION = 30

# Authentication Error Message
AUTH_ERROR_MESSAGE = (
    "Authentication failed. Refresh LEETCODE_SESSION and CSRF_TOKEN in GitHub secrets."
)

def validate_auth_config():
    if not LEETCODE_SESSION or not CSRF_TOKEN:
        raise ValueError(AUTH_ERROR_MESSAGE)
