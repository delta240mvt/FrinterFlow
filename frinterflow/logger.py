# frinterflow/logger.py
"""
Timestamped file logger for transcription entries.
"""
from datetime import datetime

import frinterflow.config as _cfg


def append_entry(text: str) -> None:
    """Append a transcribed entry with timestamp to the log file."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = _cfg.LOG_FORMAT.format(timestamp=timestamp, text=text)
    with open(_cfg.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
