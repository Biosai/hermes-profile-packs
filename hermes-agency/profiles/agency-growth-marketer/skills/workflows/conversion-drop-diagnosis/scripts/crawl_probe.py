#!/usr/bin/env python3
"""Probe what a crawler is actually served for each route of a site.

Why this exists: SPA hosts rewrite every unmatched path to index.html with
HTTP 200, so a plain status check "succeeds" on routes and files that were never
deployed. This script always fetches a deliberately impossible path as a
positive control, and discriminates robots/sitemap on content-type, not status.

Usage:
    python crawl_probe.py https://example.com
    python crawl_probe.py https://example.com --routes / /pricing /blog

stdlib only.
"""
import argparse
import gzip
import re
import urllib.request

GOOGLEBOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
CONTROL_PATH = "/this-route-cannot-exist-9x7"

DEFAULT_ROUTES = ["/", "/login", "/pricing", "/contact", "/blog"]


def fetch(url, ua=GOOGLEBOT, timeout=25):
    req = urllib.request.Request(
        url, headers={"User-Agent": ua, "Accept-Encoding": "gzip",
                      "Accept-Language": "en-US,en;q=0.9"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return r.status, r.headers.get("Content-Type", ""), raw.decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 - report, never crash the sweep
        return getattr(exc, "code", "ERR"), "", str(exc)


def visible_text(html):
    body = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    inner = body.group(1) if body else ""
    inner = re.sub(r"<script.*?</script>", " ", inner, flags=re.S)
    inner = re.sub(r"<style.*?</style>", " ", inner, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner)).strip()


def meta(html):
    def grab(pattern):
        m = re.search(pattern, html, re.S | re.I)
        return m.group(1).strip() if m else None
    return {
        "title": grab(r"<title[^>]*>(.*?)</title>"),
        "description": grab(r'<meta[^>]+name="description"[^>]+content="([^"]*)"'),
        "canonical": grab(r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", help="site root, e.g. https://example.com")
    ap.add_argument("--routes", nargs="*", default=None)
    args = ap.parse_args()
    base = args.base.rstrip("/")
    routes = list(args.routes or DEFAULT_ROUTES)
    if CONTROL_PATH not in routes:
        routes.append(CONTROL_PATH)

    print("== crawler-facing files (judge on content-type, not status) ==")
    for path in ("/robots.txt", "/sitemap.xml", "/sitemap_index.xml"):
        status, ctype, body = fetch(base + path)
        absent = "html" in ctype.lower()
        verdict = "ABSENT (SPA fallback answered)" if absent else "present"
        print(f"  {path:<20} {status}  ct={ctype[:34]:<36} {verdict}")
        if not absent and "sitemap" in path and isinstance(status, int) and status == 200:
            print(f"       <loc> entries: {len(re.findall(r'<loc>', body))}")

    print("\n== per-route view ==")
    seen = {}
    for path in routes:
        status, _ctype, html = fetch(base + path)
        if not (isinstance(status, int) and status == 200):
            print(f"  {path:<34} {status}")
            continue
        text = visible_text(html)
        m = meta(html)
        seen[path] = (len(text), m["title"])
        print(f"  {path:<34} 200  text={len(text):5d}  title={(m['title'] or 'NONE')[:46]!r}")
        print(f"       description={'YES' if m['description'] else 'NONE'}  "
              f"canonical={m['canonical'] or 'NONE'}")

    print("\n== verdict ==")
    ctrl = seen.get(CONTROL_PATH)
    if ctrl:
        print(f"  POSITIVE CONTROL {CONTROL_PATH} returned 200 with {ctrl[0]} chars "
              f"-> SPA fallback: every URL is the same document, nothing can rank.")
    else:
        print(f"  Positive control {CONTROL_PATH} did NOT return 200 -> real routing, good.")
    distinct = {v for k, v in seen.items() if k != CONTROL_PATH}
    if len(distinct) <= 1 and seen:
        print("  All probed routes share one title/body size -> duplicate content domain-wide.")


if __name__ == "__main__":
    main()
