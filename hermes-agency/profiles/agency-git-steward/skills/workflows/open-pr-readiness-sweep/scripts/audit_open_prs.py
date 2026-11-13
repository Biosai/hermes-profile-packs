#!/usr/bin/env python3
"""Audit merge-readiness of every open PR across GitHub organizations or accounts.

Read-only. Merges nothing. Writes prs_open.json and prints a tiered verdict.

Why this exists as a script: the naive version of this audit reports a false
all-clear. See the STATUS ASSERTION notes below.

GitHub only: it reads the GitHub REST API. On another code host, run the sweep
by hand with that host's CLI (see the skill's references/sweep-by-hand.md).

Usage:
    python3 audit_open_prs.py [--token-env NAME] OWNER [OWNER ...]
        OWNER is an organization or a user account. For the authenticated
        account itself, its own repositories (private ones included) are listed.
    Token: read from GITHUB_TOKEN, then GH_TOKEN, then `gh auth token`.
        --token-env NAME reads the variable NAME instead, and nothing else.
    Environment (all optional):
        GH_AUDIT_ORG      comma-separated owners, used when no argument is given
        GH_AUDIT_EXCLUDE  comma-separated owner/repo names never itemised
        GH_AUDIT_OUT      output JSON path (default prs_open.json)
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
_parser.add_argument("owners", nargs="*", metavar="OWNER",
                     help="organization or user account to sweep (default: GH_AUDIT_ORG)")
_parser.add_argument("--token-env", metavar="NAME",
                     help="read the token from this variable instead of GITHUB_TOKEN / GH_TOKEN")
ARGS = _parser.parse_args()

OWNERS = ARGS.owners or [o.strip() for o in os.environ.get("GH_AUDIT_ORG", "").split(",") if o.strip()]
if not OWNERS:
    sys.exit("usage: audit_open_prs.py [--token-env NAME] OWNER [OWNER ...]   (or set GH_AUDIT_ORG)")
EXCLUDE = {r.strip().lower() for r in os.environ.get("GH_AUDIT_EXCLUDE", "").split(",") if r.strip()}

API = "https://api.github.com"
OUT = os.environ.get("GH_AUDIT_OUT", "prs_open.json")
STANDARD_TOKEN_NAMES = ("GITHUB_TOKEN", "GH_TOKEN")


# ---------------------------------------------------------------- token
# The profile's on-disk env file is read first: a long-running process keeps
# the environment it started with, so after a rotation its variables can serve
# a revoked token for days. A token kept under another name is passed with
# --token-env NAME; then only that name is read, and a missing value is an
# error rather than a silent fall back to a different credential.
def load_token(token_env=None):
    names = (token_env,) if token_env else STANDARD_TOKEN_NAMES
    env_file = os.path.join(os.environ.get("HERMES_HOME",
                                           os.path.expanduser("~/.hermes")), ".env")
    try:
        with open(env_file) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() in names:
                    v = v.strip().strip('"').strip("'")
                    if v:
                        return v, f"file:{k.strip()}"
    except OSError:
        pass
    for k in names:
        if os.environ.get(k):
            return os.environ[k], f"env:{k}"
    if token_env:
        sys.exit(f"no GitHub token found in {token_env} (named by --token-env)")
    try:
        tok = subprocess.run(["gh", "auth", "token"], capture_output=True,
                             text=True, timeout=20).stdout.strip()
        if tok:
            return tok, "gh auth token"
    except (OSError, subprocess.SubprocessError):
        pass
    sys.exit("no GitHub token found (GITHUB_TOKEN, GH_TOKEN, --token-env NAME, or gh auth login)")


TOKEN, TOKEN_SRC = load_token(ARGS.token_env)
HDRS = {"Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "hermes-pr-audit"}


def get(path, params=""):
    """Always returns (body, status). NEVER swallow the status."""
    url = path if path.startswith("http") else API + path + params
    req = urllib.request.Request(url, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode()), r.status
    except urllib.error.HTTPError as e:
        return {"_error": e.read().decode()[:200]}, e.code
    except urllib.error.URLError as e:
        return {"_error": str(e)}, 0


# ------------------------------------------------------- controls first
me, s_pos = get("/user")
_, s_neg = get(f"/repos/{OWNERS[0]}/zzq7x4v-this-repo-does-not-exist")
print(f"token source     : {TOKEN_SRC} (len {len(TOKEN)})")
print(f"POSITIVE control : /user -> {s_pos} login={me.get('login')}")
print(f"NEGATIVE control : bogus repo -> {s_neg} (must be 404)")
if s_pos != 200 or s_neg != 404:
    sys.exit("controls failed - the probe cannot distinguish states, aborting")
LOGIN = (me.get("login") or "").lower()


# ------------------------------------------------------- enumerate repos
# An organization listing never shows repositories owned by a person, and a
# public user listing never shows that user's private ones: the authenticated
# account is listed through /user/repos instead.
def owner_listing(owner):
    if owner.lower() == LOGIN:
        return "/user/repos", "&affiliation=owner"
    _, s_org = get(f"/orgs/{owner}")
    if s_org == 200:
        return f"/orgs/{owner}/repos", "&type=all"
    return f"/users/{owner}/repos", "&type=owner"


repos = []
for owner in OWNERS:
    base, extra = owner_listing(owner)
    page = 1
    while True:
        batch, s = get(base, f"?per_page=100&page={page}{extra}")
        if s != 200 or not isinstance(batch, list) or not batch:
            if s != 200:
                print(f"  WARN {base} -> {s}")
            break
        repos += [r for r in batch if not r.get("archived")]
        if len(batch) < 100:
            break
        page += 1
excluded = sorted(r["full_name"] for r in repos if r["full_name"].lower() in EXCLUDE)
repos = [r for r in repos if r["full_name"].lower() not in EXCLUDE]
print(f"repos (non archived): {len(repos)}")
if excluded:
    print(f"excluded by GH_AUDIT_EXCLUDE (not itemised): {', '.join(excluded)}")
print()

rows = []
for r in repos:
    full = r["full_name"]
    prs, s = get(f"/repos/{full}/pulls", "?state=open&per_page=100")
    if s != 200 or not isinstance(prs, list):
        if s != 200:
            print(f"  WARN {full} pulls -> {s}")
        continue

    workflows, s_wf = get(f"/repos/{full}/actions/workflows")
    wf_names = ([w["name"] for w in workflows.get("workflows", [])
                 if w.get("state") == "active" and w.get("path", "").startswith(".github")]
                if s_wf == 200 else ["<unknown: HTTP %d>" % s_wf])

    # Branch protection is admin-only; a 403 means "I cannot know", not "no rules".
    prot, s_prot = get(f"/repos/{full}/branches/{r['default_branch']}/protection")
    required = ((prot.get("required_status_checks") or {}).get("contexts")
                if s_prot == 200 else None)

    for p in prs:
        n = p["number"]
        # 'mergeable' is absent from the list response and null on first read:
        # GitHub computes it lazily. Poll it or you get null everywhere.
        det, s_det = get(f"/repos/{full}/pulls/{n}")
        tries = 0
        while s_det == 200 and det.get("mergeable") is None and tries < 4:
            time.sleep(2)
            det, s_det = get(f"/repos/{full}/pulls/{n}")
            tries += 1

        sha = det.get("head", {}).get("sha", "")

        # STATUS ASSERTION -------------------------------------------------
        # commits/{sha}/check-runs 403s for a PAT without the `checks` scope,
        # and the 403 body has no 'check_runs' key -- so .get('check_runs', [])
        # returns [] and prints exactly like a fully green PR. Record the code.
        cr, s_cr = get(f"/repos/{full}/commits/{sha}/check-runs", "?per_page=100")
        check_runs_visible = (s_cr == 200)

        st, s_st = get(f"/repos/{full}/commits/{sha}/status")
        statuses = ([(c["context"], c["state"]) for c in st.get("statuses", [])]
                    if s_st == 200 else [])

        wf, s_wr = get(f"/repos/{full}/actions/runs", f"?head_sha={sha}&per_page=30")
        runs = ([(x["name"], x["status"], x.get("conclusion"))
                 for x in wf.get("workflow_runs", [])] if s_wr == 200 else [])

        revs, s_rv = get(f"/repos/{full}/pulls/{n}/reviews", "?per_page=100")
        approvals = (len([x for x in revs if x.get("state") == "APPROVED"])
                     if s_rv == 200 and isinstance(revs, list) else None)

        red = [x[0] for x in runs if x[2] in ("failure", "timed_out", "cancelled")]
        red += [c for c, v in statuses if v in ("failure", "error")]
        pend = [x[0] for x in runs if x[1] != "completed"]
        pend += [c for c, v in statuses if v == "pending"]
        green = ([x[0] for x in runs if x[2] == "success"]
                 + [c for c, v in statuses if v == "success"])

        row = dict(repo=full, num=n, title=p["title"], draft=p.get("draft"),
                   mergeable=det.get("mergeable"),
                   mergeable_state=det.get("mergeable_state"),
                   base=p["base"]["ref"], head=p["head"]["ref"], sha=sha[:8],
                   additions=det.get("additions"), deletions=det.get("deletions"),
                   files=det.get("changed_files"), updated=p["updated_at"][:10],
                   repo_workflows=wf_names, required_checks=required,
                   protection_http=s_prot, check_runs_http=s_cr,
                   check_runs_visible=check_runs_visible,
                   statuses=statuses, runs=runs, approvals=approvals,
                   red=red, pending=pend, green=green, url=p["html_url"])

        # CONTRADICTION GUARD ---------------------------------------------
        # mergeable_state is the free control on our own enumeration.
        row["contradiction"] = (
            det.get("mergeable_state") == "unstable" and not red and not pend)
        rows.append(row)

        flag = "  <<< CONTRADICTION: unstable but no red check found" if row["contradiction"] else ""
        print(f"{full}#{n:<5} state={str(det.get('mergeable_state')):<9} "
              f"green={len(green)} RED={len(red)} pend={len(pend)} "
              f"check-runs={s_cr}{flag}")
        if red:
            print(f"        FAILING: {red}")

with open(OUT, "w") as fh:
    json.dump(rows, fh, indent=1, ensure_ascii=False)

# --------------------------------------------------------------- verdict
print("\n" + "=" * 72)
if any(r["contradiction"] for r in rows):
    print("STOP: a PR reports 'unstable' with no failing check enumerated.")
    print("Your CI probe is blind. Fix it before reporting anything.\n")
if not any(r["check_runs_visible"] for r in rows) and rows:
    print("NOTE: check-runs was never readable (403 = missing `checks` scope).")
    print("      CI state below comes from commits/status + actions/runs only.\n")
if any(r["protection_http"] != 200 for r in rows):
    print("NOTE: branch protection unreadable (403 = not admin). 'Mergeable' below")
    print("      means git state + observed CI, NOT 'the merge button is green'.\n")

blocked = [r for r in rows if r["red"] or r["mergeable"] is not True
           or r["mergeable_state"] not in ("clean", "unstable") or r["pending"]]
ready = [r for r in rows if r not in blocked]
tested = [r for r in ready if r["green"]]
untested = [r for r in ready if not r["green"]]

print(f"TOTAL open PRs: {len(rows)}   blocked: {len(blocked)}   "
      f"mergeable: {len(ready)}\n")
print("RED / BLOCKED")
for r in blocked:
    print(f"  {r['repo']}#{r['num']} state={r['mergeable_state']} failing={r['red']}")
    print(f"      -> drill: /repos/{r['repo']}/actions/runs/<id>/jobs to name the step")
print("\nMERGEABLE - CI ran something")
for r in sorted(tested, key=lambda z: -(z["additions"] or 0)):
    d = "DRAFT" if r["draft"] else "     "
    print(f"  [{d}] {r['repo']}#{r['num']} +{r['additions']}/-{r['deletions']} "
          f"({r['files']}f) approvals={r['approvals']} workflows={r['repo_workflows']}")
print("\nMERGEABLE - nothing verifiable ran")
for r in untested:
    d = "DRAFT" if r["draft"] else "     "
    print(f"  [{d}] {r['repo']}#{r['num']} workflows={r['repo_workflows'] or 'NONE'}")

print(f"\nwrote {OUT}")
print("Now READ the workflow files of each repo before calling any of this 'green'.")
