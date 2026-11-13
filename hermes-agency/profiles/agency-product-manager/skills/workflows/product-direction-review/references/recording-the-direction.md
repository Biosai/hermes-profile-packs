# Recording the direction

Done when the owner asks to document the direction and act on it. File the items first: they carry the numbers the note cites.

## 1. The items
One item per action, each searched for duplicates across open and closed items and written to the standard of `issue-authoring-standard`.

**A build** holds:
- why, with the measured number;
- scope, and what is not in scope;
- a feature gate: the step it serves, the metric, the baseline, the read date, and the rule that removes the feature if the metric does not move;
- done-when, with the proof expected and a production check;
- any precondition ("not before the first returning user").

**An owner-only step** (a deploy, a setup only possible in a vendor's console, a merge) is an owner action: the exact steps and what it blocks. Merged work that is not deployed gets its own deploy action: until then, the gate's read date counts down on code nobody runs.

## 2. The note
Written in the knowledge base the project brief points to, on a fresh branch when it is version-controlled:
1. the awkward number first, and the statement that everything below is hypothesis;
2. the thesis, and a "substitute against us" table;
3. the smallest changes first, each mapped to an item;
4. decisions: question, answer, why, date;
5. the plan: item, owner, state, link;
6. how we will know;
7. what is dropped.

## 3. Linking
Link the note and the items both ways in the same turn. The reply gives the note's link, the ordered list with owners, and the number that decides.

## With `delivery.issue_tracker` set to `none`
The items stay in the reply and in the note, each with the same content.
