# Roast Your Own Agent (make.fun): gate the 200-char roast and stage it.
import json
import os
import sys

MY_ROAST_SLUG = "u-mfnakmal-roast-your-own-agent-2d221bda"
MY_ROAST_TASK = "Roast Your Own Agent"
MY_ROAST_CAP = 200
MY_ROAST_BATCH = "roast-r32-1126"


def validator():
    roast_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    with open(roast_file, encoding="utf-8") as handle:
        return handle.read().strip()


def checker(text):
    def inner():
        return text, 1 <= len(text) <= MY_ROAST_CAP

    return inner()


def stager(text):
    spot = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(spot, exist_ok=True)
    with open(os.path.join(spot, "entry.txt"), "w", encoding="utf-8", newline="\n") as out:
        out.write(text + "\n")


def announcer(text, good):
    body = {"outcome": "clean" if good else "dirty", "slug": MY_ROAST_SLUG, "task": MY_ROAST_TASK, "len": len(text), "batch": MY_ROAST_BATCH}
    print(json.dumps(body))
    print("roast registered under batch", MY_ROAST_BATCH)


roast = validator()
_text, good = checker(roast)
if not good:
    announcer(roast, False)
    sys.exit(6)
stager(roast)
announcer(roast, True)
