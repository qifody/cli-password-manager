import os
from datetime import datetime


def log_event(event, logfile):
    log_dir = os.path.dirname(logfile)

    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"{timestamp}\t{event}"

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")