#!/usr/bin/env python3
"""Measure what a visitor must download before seeing anything.

This is the step that gets skipped and is often the whole answer: if the landing
page is a client-rendered SPA that needs ~300KB of blocking JS, and the median
session in the analytics source is a few seconds, visitors leave around the moment
the page finishes rendering. No targeting or copy change fixes that.

The user agent is required: probe as the traffic you are diagnosing really arrives.
Use a preset with --ua, or pass any other user agent in full with --ua-string
(copy it from the analytics source or the server logs).

Usage:
  python landing_payload.py https://example.com --ua android
  python landing_payload.py https://example.com --ua iphone --mbps 1.5
  python landing_payload.py https://example.com --ua desktop --path /login
  python landing_payload.py https://example.com --ua-string "Mozilla/5.0 (...) SomeApp/1.0"
"""
import argparse
import re
import time
import urllib.error
import urllib.request

UAS = {
    "instagram": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Mobile/15E148 Instagram 300.0.0.0"),
    "facebook": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
                 "(KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBAV/450.0.0.0]"),
    "iphone": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
               "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"),
    "android": ("Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Mobile Safari/537.36"),
    "desktop": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
}

# Mount-only bodies: nothing is visible until JS executes.
MOUNT_RE = re.compile(
    r'<body[^>]*>\s*(<div\s+id="(root|app|__next|__nuxt)"[^>]*>\s*</div>\s*)+',
    re.I,
)


def fetch(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip, br"})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=30)
        body = r.read()
        return len(body), (time.time() - t0) * 1000, r.status, r.headers.get("content-encoding", "-"), body
    except urllib.error.HTTPError as e:
        return 0, 0, f"HTTP {e.code}", "-", b""
    except Exception as e:  # noqa: BLE001
        return 0, 0, type(e).__name__, "-", b""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("base")
    who = p.add_mutually_exclusive_group(required=True)
    who.add_argument("--ua", choices=sorted(UAS),
                     help="preset user agent of the traffic being diagnosed")
    who.add_argument("--ua-string", metavar="USER_AGENT",
                     help="any other user agent, in full")
    p.add_argument("--path", default="/")
    p.add_argument("--mbps", type=float, default=1.5,
                   help="effective mobile throughput for the time estimate")
    a = p.parse_args()

    base = a.base.rstrip("/")
    ua = UAS[a.ua] if a.ua else a.ua_string
    label = a.ua or f"custom ({ua[:60]})"

    n, ms, st, enc, body = fetch(base + a.path, ua)
    html = body.decode("utf-8", "replace")
    print(f"UA: {label}")
    print(f"HTML{'':<52}{n:>9,} B  {ms:6.0f} ms  {st}  enc={enc}")

    # Only head-referenced assets block first paint.
    head = html.split("</head>")[0]
    assets = list(dict.fromkeys(re.findall(r'(?:src|href)="(/[^"]+\.(?:js|css|mjs))"', head)))

    total, js_total, css_total = n, 0, 0
    print(f"\n{len(assets)} render-blocking assets in <head>:")
    for path in assets:
        an, ams, ast, aenc, _ = fetch(base + path, ua)
        total += an
        if path.endswith(".css"):
            css_total += an
        else:
            js_total += an
        warn = "  <-- uncompressed" if aenc == "-" and an > 2000 else ""
        print(f"  {path:<54}{an:>9,} B  {ams:6.0f} ms  enc={aenc}{warn}")

    print(f"\nTOTAL before first paint: {total:,} B = {total / 1024:.0f} KB "
          f"(JS {js_total / 1024:.0f} KB, CSS {css_total / 1024:.0f} KB)")
    secs = total * 8 / (a.mbps * 1_000_000)
    print(f"Download alone at {a.mbps} Mbps: ~{secs:.1f}s, BEFORE parse/exec.")
    print(">>> Compare this with the median session duration of that traffic in the")
    print(">>> analytics source. If they are the same order of magnitude, rendering may")
    print(">>> be the bottleneck: prove it with a before/after before ranking it first.")

    # Server-rendered text: what a crawler, a link preview, or a slow phone sees.
    body_html = html.split("<body", 1)[1] if "<body" in html else ""
    body_html = re.sub(r"<script\b.*?</script>", "", body_html, flags=re.S | re.I)
    body_html = re.sub(r"<style\b.*?</style>", "", body_html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = re.sub(r"\s+", " ", text).strip()
    print(f"\nHuman-readable text in served HTML body: {len(text)} chars")
    if MOUNT_RE.search(html) or len(text) < 200:
        print("  !! CLIENT-RENDERED ONLY: the body is an empty mount point.")
        print("  !! Nothing paints until the JS bundle downloads, parses and runs.")
        print("  !! Crawlers and social link previews also see nothing.")
        print("  !! Fix = SSR/prerender, or inline a static hero in index.html.")
    else:
        print(f"  preview: {text[:200]!r}")


if __name__ == "__main__":
    main()
