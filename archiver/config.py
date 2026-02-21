GRAPHQL_URL = "https://leetcode.com/graphql"

# 🔐 Paste fresh cookies before running
LEETCODE_SESSION = "PASTE_YOUR_LEETCODE_SESSION"
CSRF_TOKEN = "PASTE_YOUR_CSRF_TOKEN"

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