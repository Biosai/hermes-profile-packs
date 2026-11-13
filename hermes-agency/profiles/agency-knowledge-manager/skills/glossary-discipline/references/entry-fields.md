# The entry fields

Every glossary entry holds all six. An entry with a field left out is a draft.

| Field | What it holds |
|---|---|
| **Term** | the one word or phrase the team uses |
| **Definition** | one or two sentences saying what the concept is for, in other glossary terms where possible |
| **Code names** | the identifiers that carry it (table, type, enum, API field), each cited `path:line @ <commit>` at the default branch; when the code uses another word, the mapping |
| **Banned synonyms** | the words not to use for this concept, and why when it is not obvious |
| **Not to be confused with** | neighbouring terms, and the difference |
| **Stable id** | an id that never changes, so documents link the entry instead of redefining the term |

## A correction
One line per wrong use, posted where `delivery.issue_tracker` says:

```
Term: <used> -> <glossary term> (<entry link>) at <location>
```
