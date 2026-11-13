# Unfinished work

Companion to `bounded-task-delivery`. Written code never stays only on a local disk.

- Commit unfinished work and push it as a draft pull or merge request.
- Its description opens with what fails: the failing suites and why, and the passing count.
- It says "do not merge" and names the work item that finishes it.
- It lists what is deliberately absent, and the decisions worth challenging now.
- Post the measured CI conclusion as a comment on the request.
- Split a finished fix from unfinished work into two requests: check the finished paths out onto
  the right base.
- A pushed branch that is ahead of the default branch and has no request is a missing request or
  dead weight: raise it.
- When your own sequencing was wrong, say so in the reply.
