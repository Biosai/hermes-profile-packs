# Probing a conversion step against production

How to settle "is this step broken, or did nobody try?" with a real call instead of a code
reading. Reading the handler tells you what it *would* do; only a request tells you what it
does. A defect found by inspection is not evidence of the outage you are chasing.

Run it only with the owner's standing approval for production probes: it creates a real
account and real rows. Use an obviously fake address on a reserved domain (`@example.com`)
and a random password, so a row that survives cleanup is identifiable.

## 1. Recover public client config from the shipped bundle

Visitors run the deployed artifact, not a working copy; a local `.env` can differ.

```bash
curl -sL https://example.com/ | grep -oE '/assets/[A-Za-z0-9._-]+\.js'   # asset paths
# download every asset, then grep the set for the public key or API base URL you need
```

Web API keys and API base URLs in a client bundle are public by design; recovering them is
not credential handling. Never do this for server secrets. Config often sits in a lazily
loaded chunk, not the entry file: grep every asset, or you will conclude the value is absent.

## 2. Mint a real credential the way the client does

Use the auth provider's public REST API, the same one its SDK wraps (for example an
`accounts:signUp`-style call with the web key), and keep the returned token.

## 3. Call the conversion endpoint

Send the token plus the headers a browser sends, `Origin` in particular, or you are not
exercising the CORS path the visitor hits. Assert on the status code:

| Result | Meaning |
|---|---|
| 2xx | The step works. The deficit is arrival or intent. |
| 401/403 | Auth wiring: token audience, guard. |
| other 4xx | Contract mismatch: validation, a required field. |
| 5xx | Server fault; read the handler's catch-all before concluding. |

A 5xx on a deliberately invalid token proves nothing about the valid path: broad catch
blocks map every error to 500. That is a separate observability bug, not the constraint.

## 4. Continue to the payment provider

With the same token: list the product the paywall sells, create a checkout, assert the
session is live (for Stripe `cs_live_`, not `cs_test_`, which means test keys in production),
and GET the checkout URL with a browser user agent to see it load. An unpaid checkout
session expires on its own. Without this step, "signup works" says nothing about revenue.

## 5. Clean up, always, in the same script

Delete the application row first, authenticated as the probe (the app's delete route needs
the still-valid token), then the auth user, then check that the profile endpoint now
answers 404. A `404 Cannot DELETE` means you guessed the route: find it in the code. If a row
cannot be removed, report its id and offer the query. Never claim a half-done cleanup.

## 6. Read the response body, not only the status

Compare server-stamped fields with the wall clock. A `created_at` weeks off on a row created
a second ago is a clock, timezone or default-value defect, and every database count dated
by that column is suspect. Probe twice: two rows minutes apart with the same timestamp point
to a default evaluated once at process start (an ORM default of `new Date()` instead of the
per-insert sentinel). Rows already written cannot be repaired; date series from analytics.

## Re-run, don't cite

"Can a user do X in production right now?" gets a fresh probe. An earlier result is context.

## Is the merged fix running?

Check for a deploy pipeline before assuming merge = live; with none, deploys are manual.
Fingerprint the live build from a contract change the fix introduced (a new response code in
the served API description) and re-probe the behaviour itself.

## Ruling out infrastructure changes near the drop

Security hardening merged days before a metric fell is a seductive false lead. Test it.

```bash
for O in https://example.com https://www.example.com https://evil.example; do
  curl -s -i -X OPTIONS https://api.example.com/users -H "Origin: $O" \
    -H "Access-Control-Request-Method: POST" | grep -i access-control-allow-origin
done
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' https://www.example.com/
for i in $(seq 1 12); do curl -s -o /dev/null -w '%{http_code} ' https://api.example.com/products; done
curl -s -I https://api.example.com/products | grep -i x-ratelimit
```

A host refused by a CORS allowlist is harmless when it redirects to the canonical origin
before any script runs. Check the redirect before indicting the allowlist.
