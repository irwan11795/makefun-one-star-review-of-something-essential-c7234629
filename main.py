"""One-Star Review of Something Essential entry for make.fun.

Writes a single deadpan one-star review line to /output/entry.txt.
Python 3 standard library only, deterministic, no network, no file reads.
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY = "One star. Sleep takes eight hours a night and still delivers me to the morning tired, late, and rehearsing arguments from 2014."


def _validate_entry(text):
    """Gate: entry must be non-empty, non-whitespace, 1-160 chars."""
    if not text or not text.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        return False
    if len(text) > 160:
        print(
            "error: entry is %d characters, exceeds 160" % len(text),
            file=sys.stderr,
        )
        return False
    return True


def _candidate_dirs():
    """Output directories in fallback order."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(Path(env_dir))
    dirs.append(Path("/output"))
    dirs.append(Path(__file__).resolve().parent / "output")
    dirs.append(Path(tempfile.gettempdir()))
    return dirs


def main():
    if not _validate_entry(ENTRY):
        return 1
    for directory in _candidate_dirs():
        try:
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / "entry.txt"
            target.write_text(ENTRY, encoding="utf-8")
            return 0
        except OSError:
            continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
