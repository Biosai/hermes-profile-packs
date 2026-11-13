# Auditing public surfaces into items

Companion to `repo-audit-to-issues`. A dormant project usually has a public surface: a site, a
social account, a launch plan, a domain, community invites. That surface makes claims, and the
claims are auditable against the code with the same evidence standard as a failing test. The
output is still items, not changes: even an obvious one-line fix goes into the item as a quoted
diagnosis, and you keep producing items until told otherwise.

## Cross-reference the surface against the repository
The finding is rarely in one place; it is in the contradiction between two.

| Check | What it catches |
|---|---|
| Last public post date against the last commit date | the whole project stopped on one day, not "the account drifted" |
| Engagement read as a series | a declining series measures the audience's response and pre-empts "just post more" |
| Social and contact URLs grepped from the app config | a footer sending every click to a stranger's account: a live leak that outranks the rest |
| Shipped claims against deployed state | "coming soon" while every contract address or endpoint is still a placeholder |
| Claims against the project's own compliance documents | investment or scarcity vocabulary on a product that committed never to use it |
| The plan's targets against measured reality | a plan whose launch-week target is a thousand times the measured total is not a restart plan |

Let the surface win when it is more correct than the docs (posts naming the platform the code
migrated to while the strategy doc still names the old one), and write that direction into the
item so nobody "fixes" the right artifact. Say what is accurate and worth keeping.

Split two decisions into two items: the mechanics (a wrong handle in the footer, naming
inconsistencies, profile assets, cadence) and the truthfulness (what may be claimed today,
whether existing posts stay up, a copy rule set consistent with the project's own compliance
posture). Bundled, nobody can act on it.

When the agent lacks the credentials to read a surface, say so in the item and in the report,
point at the item that already tracks the same class of gap, and offer what is possible ("I can
draft; publishing stays manual"). Attribute a screenshot the owner sent as such; it is not an API
measurement. End the report with the questions only the owner can answer, unanswered.

## Live destinations: links, invites, handles
Dead-and-real often returns exactly what fake-and-nonsense returns.
- A service that answers the same error for a dead target and a nonsense string (an invite API
  returning one "unknown invite" body for both) needs positive controls: well-known live targets
  that return 200 beside the target's error.
- A service that answers 200 for everything (profile pages with a plausible title for any name)
  makes the status, title and preview tags useless. Diff a known-real page against a known-fake
  one, find the marker that differs, and test that marker.
- Run both controls in the same script and run, printed beside the result, so the item carries
  the proof that the check works.

A destination must exist before traffic is driven to it: trace teaser, click, dead end, and say
that attention is being spent rather than accumulated. Offer the zero-setup option (remove the
dead links) beside real destinations in increasing order of effort, and cite a sibling project
that already failed this way if there is one.

## Domain and name availability
The default failure reports free names as taken, silently. A WHOIS answer that does not contain
"not found" may be "TLD is not supported", "no data found" or a DNS failure for the WHOIS host:
none is a registration.
- Use registry RDAP resolved through the IANA bootstrap file (`https://data.iana.org/rdap/dns.json`)
  and read the HTTP status: 404 is free, 200 is registered, anything else is unknown and reported
  as unknown. Do not start from a redirector: its 404 for a TLD without RDAP means "no RDAP
  here", not "free". Without an RDAP base, use that registry's own WHOIS host on port 43.
- Controls in both directions, on the same TLD as each target: a name known to be taken must read
  taken, and a nonsense name must read free. A positive control alone passes a check that answers
  "taken" to everything.
- An expired name is not buyable yet. `server hold` means it is out of the zone (confirm with DNS
  returning NXDOMAIN); `pending delete` lasts a fixed five days, so the drop date is about the
  last change plus five days, stated as an estimate; parking nameservers mean drop-catchers watch
  it. A manual registration at drop time usually loses: the action is a backorder placed before
  the drop. A registrar that is not the project's means a third party owns it, and any hard-coded
  reference to it in the code is an assumption, not ownership.
- Price the free alternatives beside the contested name, and fold in adjacent gaps: register under
  the company rather than a person, set SPF and DMARC before any mail is sent, update hard-coded
  hostnames, and replace legal placeholders that need an address on the new domain.

## Community surfaces and third-party platforms
- A platform that will process members' data (handles, messages, joins) is a data processor:
  check the project's records of processing and impact assessments before writing the item, and
  add a scope line to record it, with proportionate weight ("not a blocker for a soft launch,
  cheap now, expensive after launch").
- Do not mirror a large configuration constant into real-world structure: hundreds of supported
  cities do not mean hundreds of channels. Empty rooms read as a dead community; promote one when
  it has the people.
- Name the prerequisite before the build: who moderates. Include the hardening steps as scope
  items (restrict posting, disable member messages, raise verification, a non-expiring invite).

## Access requests for the agent
Build the capability table first: which tasks already work without the access, and which it truly
unblocks (often replying and measuring, not posting). Put that framing in the item title so the
request is not read as convenience. Cost it in scenarios from the platform's published price list,
not as one number: per-call pricing can make one post format cost many times another, and
read-heavy polling is usually the only real cost risk. Write the setup steps and the platform's
known traps into the item so the owner can act without a round trip. Secrets are entered by the
owner in a terminal, never pasted into chat. Record the guardrails that survive the access
(publishing stays manual, a reply is a public statement under the same copy rules).
