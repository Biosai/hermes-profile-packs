# Organic and owned-channel audit

Use when the ask is "how do we get organic traffic", "should we redo the app page", "why is
search flat", or any proposal to invest in content. The question is almost never what to
write; it is whether the channel can carry anything at all.

## 1. Size the channel before diagnosing it

Pull the channel groups over 90 days with each one's share, then non-paid source and medium
over 365 days.
- Organic search in single digits per quarter: an indexation or crawlability problem, not a
  ranking one. Go to step 2.
- A referral source with long sessions and several pages per session (a directory, an
  aggregator) is the compounding thing that already works. Name it.

A 90% or higher paid share is a finding in itself: the traffic stops the day spending stops.

## 2. Probe what a crawler is served

`python3 scripts/crawl_probe.py <site> --routes / /pricing /blog` fetches each route with a
crawler user agent and always adds an impossible path as a positive control. It probes as a
neutral crawler unless told otherwise: add `--crawler <name>` for a search crawler it has a
preset for (`--help` lists them), or `--ua-string "<full user agent>"` for any other, when the
site may serve known crawlers a different page. Say in the report which one was used.

| Observation | Diagnosis | Action |
|---|---|---|
| The impossible path returns 200 with homepage content | single-page-app fallback; every URL is one document | fix routing or pre-rendering before any content work |
| Every route shares one title and description | duplicate content domain-wide | per-route metadata at build time |
| `robots.txt` or `sitemap.xml` answers 200 with `text/html` | the files are absent; the fallback answered | real static files; judge on content type, not status |
| Canonical present in the running app, absent from served HTML | injected at runtime, invisible to crawlers | emit it at build time |
| Body text identical on every route | one pre-rendered shell | decide per-route pre-rendering (step 3) |

Look in the host's redirect configuration for a catch-all rewrite to `index.html` with status
200: with build-time pre-rendering it serves duplicate content everywhere and never a 404.

## 3. Separate the free half from the expensive half

- Free: a static `robots.txt` with a `Sitemap:` line, a generated sitemap of public routes
  only, a build-time canonical; signed-in routes excluded and marked `noindex`.
- Expensive: per-route pre-rendering multiplies build output and translations. Present it as
  a trade-off for the owner to decide, never before the free half ships.

## 4. Rank written-but-unpublished assets first

Store listings, profile copy or directory entries sitting in a repository produce nothing.
Verify on the live public page: title, description, install or rating counters. Publish, let
it run, baseline, then test a variant. A prepared listing pays back in days, indexation in
months: order the answer accordingly.

## 5. Name the access you do not have

Search-console coverage (pages indexed, manual actions) sharpens the priority and is often
not connected. Say so in one line and what it would change.

## Filing

One root cause, one tracker item. Search existing items by body text for distinctive terms
(`robots.txt`, `sitemap`, `canonical`, `soft 404`) across open and closed, and run a term you
know exists as a positive control before trusting "no duplicates".
