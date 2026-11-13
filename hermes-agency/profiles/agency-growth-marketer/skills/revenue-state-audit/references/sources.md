# Reading each source

Read-only in every case. For each number, record the source, the query or export used, the window and the time it was run. This skill bundles no reader script: where a connector exists, use it; otherwise use the source's own API or export by hand, and say in the report which one was used.

## Analytics (`growth.analytics_source`)
| Value | How to read it | Access to ask for |
|---|---|---|
| `ga4` | a connector, or the property's reporting API; otherwise a report export | Viewer on the property; with no connector, a service-account file named in `GOOGLE_APPLICATION_CREDENTIALS` |
| `plausible` | its stats API, or the dashboard's export | a read-only API key, or a shared dashboard link |
| `posthog` | its query API or a saved insight, or an export | a personal API key limited to read scopes |
| `matomo` | its reporting API, or a report export | a token of a user with view access |
| `other` | ask the owner which tool it is, and whether it has an API or only an export | the tool's read-only role |
| `none` | nothing is read | none |

What to pull, whatever the source: sessions and people per day; the same by channel, device and country; session duration and pages per session; each funnel event counted as people; the date each event was first recorded.

With `none`, nothing can be concluded about arrival, channels, the paid share, or where visitors stop before signup. The user store, when readable, still gives signups and activation.

## Payments (`growth.payments_source`)
| Value | How to read it | Access to ask for |
|---|---|---|
| `stripe` | a connector, or its API; otherwise a dashboard export | a restricted key with read-only permissions, in `STRIPE_API_KEY` when there is no connector |
| `paddle` | its API, or a report export | a key with the narrowest read permissions the account offers |
| `lemonsqueezy` | its API, or an export of orders and subscriptions | a key, or the export when a key cannot be limited to reading |
| `other` | ask the owner which provider it is, and whether it has an API or only an export | the provider's read-only role |
| `none` | nothing is read | none |

What to pull, whatever the source: completed payments with the amount actually paid and the date; subscriptions with the amount paid on their latest invoice; checkouts started against checkouts completed; refunds; and whether each record is live or test.

With `none`, nothing can be concluded about revenue, about who paid, or about whether the pay path works past the checkout page.

## When a key cannot be read-only
Prefer the export. A key that can write is an owner decision: ask, and never store it outside the place the owner chose.
