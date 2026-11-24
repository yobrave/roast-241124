#!/usr/bin/env python3
"""rop2 reentry: copy the roast line into the site output folder."""
import json
import os
import sys

LIMIT = 140
TAG = "rop2-reentry-2seconds-promise"


def fetch_line():
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, "entry.txt"), encoding="utf-8") as fh:
        blob = fh.read()
    for row in blob.splitlines():
        row = row.strip()
        if row:
            return row
    return ""


def verdict(ok, chars=0, why=""):
    payload = {"status": "ok" if ok else "bad", "tag": TAG, "limit": LIMIT, "chars": chars}
    if why:
        payload["why"] = why
    print(json.dumps(payload))


def start():
    line = fetch_line()
    size = len(line)
    if size == 0 or size > LIMIT:
        verdict(False, size, "line length outside 1..%d" % LIMIT)
        sys.exit(2)
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(folder, exist_ok=True)
    dest = os.path.join(folder, "entry.txt")
    with open(dest, "w", encoding="utf-8", newline="\n") as sink:
        sink.write(line + "\n")
    with open(dest, encoding="utf-8") as mirror:
        echo = mirror.read().strip()
    if echo != line:
        verdict(False, size, "written file does not match source line")
        sys.exit(2)
    verdict(True, size)


start()
