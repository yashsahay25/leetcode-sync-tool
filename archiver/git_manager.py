import os
import subprocess
from datetime import datetime
from .logger import log

def commit_file(file_path, message, timestamp):
    dt = datetime.utcfromtimestamp(int(timestamp))
    formatted = dt.strftime("%Y-%m-%dT%H:%M:%S")

    os.environ["GIT_AUTHOR_DATE"] = formatted
    os.environ["GIT_COMMITTER_DATE"] = formatted

    subprocess.run(["git", "add", file_path])
    subprocess.run(["git", "commit", "-m", message])

    log(f"Committed: {file_path} at {formatted}")