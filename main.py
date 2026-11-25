"""Operator roast line, reentry 0822.

os.path pipeline over raw bytes: load entry.txt from this script's
directory, split off the first non-blank line, hold it to the 140
character gate, copy it into the grader's output directory, confirm
the copy, and print a single JSON result line.
"""
import json
import os
import os.path

SRC = "entry.txt"
OUT = "entry.txt"


def go():
    home = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(home, SRC), "rb") as fh:
        blob = fh.read()
    blob = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    line = b""
    for chunk in blob.split(b"\n"):
        if chunk.strip():
            line = chunk
            break
    text = line.decode("utf-8")
    CAP = 140  # sealed scorer bound for this bounty
    assert 1 <= len(text) <= CAP, "gate: line spans %d chars, needs 1..%d" % (len(text), CAP)
    yard = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(yard, exist_ok=True)
    dest = os.path.join(yard, OUT)
    with open(dest, "wb") as fh:
        fh.write(line)
    with open(dest, "rb") as fh:
        assert fh.read() == line, "readback differs"
    print(json.dumps({"result": "ok", "n": len(text)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(go())
