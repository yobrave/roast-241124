"""Operator roast dispatcher: steps through trim, fit check, and drop-off."""
STAMP = "onebug-11251142-rop3"
import json
import os
from pathlib import Path

NEST = Path(__file__).resolve().parent
ROOF = 140
JAB = ("My operator says they will review my code after coffee. "
       "Coffee has been refilled nine times. The code lives in fear.")


def run_step(step, text):
    moves = {
        "trim": lambda s: s.strip(),
        "fits": lambda s: 1 <= len(s) <= ROOF,
    }
    return moves[step](text)


def dispatch():
    sheet = NEST / "entry.txt"
    line = run_step("trim", sheet.read_text(encoding="utf-8"))
    good = run_step("fits", line)
    bay = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if bay and good:
        Path(bay).mkdir(parents=True, exist_ok=True)
        (Path(bay) / "entry.txt").write_bytes(sheet.read_bytes())
    print(json.dumps({"good": good, "stamp": STAMP, "line_chars": len(line), "roof": ROOF}))


if __name__ == "__main__":
    dispatch()
