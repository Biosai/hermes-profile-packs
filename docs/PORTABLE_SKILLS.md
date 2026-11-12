# Portable skills: configuration and prerequisites

A skill in this repository must work for a team it has never met. One team has a monorepo, another ten repositories. One tracks work in GitHub Issues, another in Jira, a third nowhere. One merges after review, another only on the owner's word. A skill that hard-codes any of this is wrong for most of its users.

This convention applies to every skill added by this fork: the Agency and Council additions, `shared-skills/`, the two new Agency profiles and `hermes-property`. Upstream skills are left as they are.

## 1. Settings, not assumptions

Anything that differs between setups is a **setting** declared in the skill's frontmatter under `metadata.hermes.config`. Hermes stores the value in the profile's `config.yaml` under `skills.config.<key>` and shows the resolved values to the agent as a `[Skill config: …]` block every time the skill is loaded; an unset key shows its declared default. Set a value with `hermes config set skills.config.<key> <value>` (for one profile: `hermes -p <profile> config set …`), and let `hermes config migrate` prompt for every declared key that is still unset. (`hermes skills config` is a different command: it only enables or disables skills.)

Keys are shared: two skills that declare `delivery.issue_tracker` read the same value. Use the registry below rather than inventing a near-duplicate key.

```yaml
---
name: ready-to-merge-gate
description: "Decide if a change is ready to merge, with evidence"
metadata:
  hermes:
    config:
      - key: delivery.code_host
        description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect"
        default: "detect"
      - key: delivery.merge_policy
        description: "Who merges: owner, reviewer, or auto-when-green"
        default: "owner"
---
```

In the body, a `## Configuration` section says how each value changes the procedure, and what the skill does when a value is `detect` or unset: detect it (say how), state what was detected, and suggest the `hermes config set skills.config.<key> <value>` line that makes it permanent. Never silently fall back to one team's habit.

### Key registry

| Key | Values | Default | Meaning |
|---|---|---|---|
| `delivery.code_host` | github, gitlab, bitbucket, other, detect | detect | Where code and reviews live. Decides the CLI (`gh`, `glab`, …) and the words (pull request vs merge request). Detect from `git remote get-url origin`. |
| `delivery.repo_layout` | single, monorepo, multi-repo, detect | detect | How the code is split across repositories. Monorepo: scope every change, test run and CI filter to the affected packages. Multi-repo: a change may span repos; link them. |
| `delivery.repos` | paths or URLs, comma-separated | (empty: current directory) | The working copies this profile may read or change. |
| `delivery.default_branch` | a branch name, detect | detect | The repository's default branch. Detect with `git symbolic-ref --short refs/remotes/origin/HEAD`; never assume `main`. |
| `delivery.issue_tracker` | github, gitlab, jira, linear, file, none, detect | detect | Where findings and work items go. `file`: a Markdown file named in `delivery.issue_file`. `none`: findings go in the report, never into a tracker. |
| `delivery.issue_file` | a path | (empty) | The Markdown file that holds work items. Used only when `delivery.issue_tracker` is `file`. |
| `delivery.board` | hermes-kanban, tracker, none | none | Where the team claims work. `none`: skip board steps and say so. |
| `delivery.merge_policy` | owner, reviewer, auto-when-green | owner | Who may merge. A profile never merges under `owner`. |
| `delivery.iac_tool` | terraform, opentofu, pulumi, cloudformation, other, none, detect | detect | Infrastructure-as-code tool, when there is one. |
| `delivery.apply_policy` | human, pipeline-after-approval | human | Who applies infrastructure changes. A profile never applies under `human`. |
| `owner.channel` | free text | this conversation | Where questions and owner actions reach the owner. |
| `owner.action_tracker` | issue-tracker, file, conversation | conversation | Where an owner action is recorded while it waits. |
| `venture.brief` | a path or URL | (empty: ask) | The venture's brief: customer, voice, constraints, autonomy. |
| `growth.analytics_source` | ga4, plausible, posthog, matomo, other, none | none | Where traffic and funnel numbers come from. |
| `growth.payments_source` | stripe, paddle, lemonsqueezy, other, none | none | Where revenue numbers come from. |
| `publishing.approval` | hermes-approval, explicit-message | explicit-message | How the owner's approval of an outward action is captured. |
| `books.format` | beancount, hledger, ledger, spreadsheet, detect | detect | Bookkeeping file format. |
| `books.location` | a path | (empty: ask) | Where the books live. |
| `training.record` | memory, a file path, an app export | memory | Where the training log lives. |
| `property.investor_file` | memory, a path | memory | Where the investor's profile and own rules live. |
| `property.question_register` | memory, a path | memory | Where open questions and answers are recorded. |
| `property.jurisdictions` | e.g. `BE-WAL,BE-BRU,BE-VLA,FR`, detect | detect | Regions and countries in play. Detect from the property's address, then confirm. |
| `property.cost_library` | a path, none | none | The work-item cost library, when one exists. |

Add a key only when no row fits, and add it to this table in the same change.

## 2. Prerequisites, declared and checked

A skill that needs access says so before it starts, and stops cleanly without it.

**In the frontmatter**, declare what Hermes can check:

- `required_environment_variables`: credentials the skill reads from the environment. Hermes marks the skill "setup needed" and prompts for them. Use `optional: true` when the skill has a documented fallback.
- `required_credential_files`: credential files, such as a service-account JSON.
- `metadata.hermes.prerequisites.commands`: CLIs the procedure runs (informational today; still list them).

```yaml
required_environment_variables:
  - name: GA4_PROPERTY_ID
    prompt: "GA4 property id (numbers only)"
    help: "Admin > Property settings in Google Analytics"
    required_for: "reading traffic and conversions from GA4"
    optional: true
```

**In the body**, a `## Prerequisites` section, right after the opening, lists each need with why it is needed and a one-line check:

| Needs | Why | Check |
|---|---|---|
| Read access to the GA4 property (Viewer) | traffic and conversion numbers | a 1-day report for the property returns rows |
| `gh` authenticated with repo read | PR state and CI logs | `gh auth status` |

Then the rule, in these words or equivalent:

> If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

A prerequisite that depends on a setting is conditional: "GA4 access, when `growth.analytics_source` is `ga4`".

## 3. Wording

- Name the concept, not one team's tool: "the issue tracker", "the code host", "the default branch", "the coordination board", "the pull or merge request". Give tool-specific commands only as examples, per `delivery.code_host`.
- No paths, hosts, channels, repositories or product names from any real team.
- `description` is at most 60 characters, quoted, and starts with what the skill does: Hermes clips longer descriptions in the skill index the agent chooses from.
- Frontmatter must be valid YAML. Quote any value containing `: `.
