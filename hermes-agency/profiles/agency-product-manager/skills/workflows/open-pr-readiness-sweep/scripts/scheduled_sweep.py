#!/usr/bin/env python3
"""Scheduled PR readiness snapshot: a wrapper around audit_open_prs.py.

Why a wrapper rather than scheduling the auditor directly:

  1. DETERMINISM. Change detection is only meaningful if identical state
     produces identical bytes: rows are sorted by (repo, num) and no timestamp
     is printed in the body.
  2. A STRUCTURED TAIL. The agent turn reasons over JSON fields instead of
     re-parsing the prose the auditor printed.
  3. A CONTROL GATE, the important one. A revoked token or a network fault
     makes the auditor report ZERO open PRs, which reads as a clean "nothing to
     review". If the auditor's own positive and negative controls did not run,
     this exits non-zero with the raw output instead of an empty table.

Environment:
    PR_SWEEP_ORG      owners to sweep, comma-separated (required); passed to
                      the auditor as GH_AUDIT_ORG
    PR_SWEEP_WORKDIR  where prs_open.json is written
                      (default: $HERMES_HOME/cache/pr-sweep, or ~/.hermes/...)
    GH_AUDIT_EXCLUDE  owner/repo names never itemised (read by the auditor)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDITOR = os.path.join(HERE, "audit_open_prs.py")
ORG = os.environ.get("PR_SWEEP_ORG", "").strip()
WORK = os.environ.get("PR_SWEEP_WORKDIR") or os.path.join(
    os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "cache", "pr-sweep")

# The auditor's key is `num`. Reading "number" yields None for every row while
# the table still looks structurally correct: verify a real number appears.
FIELDS = ("repo", "num", "title", "draft", "mergeable", "mergeable_state",
          "green", "red", "approvals", "updated", "url")


def main():
    if not ORG:
        print("ERROR: PR_SWEEP_ORG is not set: no owner to sweep. No verdict.")
        return 1
    if not os.path.exists(AUDITOR):
        print(f"ERROR: auditor script missing at {AUDITOR}")
        return 1
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, "prs_open.json")
    # A previous run's file must never stand in for this run's result.
    if os.path.exists(path):
        os.remove(path)

    env = dict(os.environ, GH_AUDIT_ORG=ORG)
    try:
        r = subprocess.run([sys.executable, AUDITOR], cwd=WORK, env=env,
                           capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        print("ERROR: auditor timed out after 600s. No verdict.")
        return 1

    out = r.stdout or ""

    # --- CONTROL GATE: refuse to emit a reassuring empty table -------------
    # "login=None" after a 401 still contains "login=": require the 200 itself.
    if "POSITIVE control : /user -> 200" not in out:
        print("ERROR: the auditor's positive control did not pass: output unusable.")
        print("This is NOT 'no open PRs'. Check the token before believing anything.")
        print(out[-1500:])
        print((r.stderr or "")[-800:])
        return 1
    if "NEGATIVE control : bogus repo -> 404" not in out:
        print("ERROR: negative control failed: the client cannot tell 404 from 200.")
        print(out[-1500:])
        return 1

    if r.returncode != 0:
        print(f"ERROR: the auditor exited with status {r.returncode}: no verdict.")
        print(out[-1500:])
        print((r.stderr or "")[-800:])
        return 1

    print(out.strip())

    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                rows = json.load(fh)
        except (OSError, ValueError) as e:
            print(f"(could not read prs_open.json: {type(e).__name__}: {e})")
            return 1
        print("\n--- STRUCTURED ---")
        for x in sorted(rows, key=lambda d: (d.get("repo", ""), d.get("num") or 0)):
            print(json.dumps({k: x.get(k) for k in FIELDS},
                             ensure_ascii=False, sort_keys=True))
        if rows and all(x.get("num") is None for x in rows):
            print("WARNING: every PR number is null: wrong JSON key, output unusable.")
            return 1
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
