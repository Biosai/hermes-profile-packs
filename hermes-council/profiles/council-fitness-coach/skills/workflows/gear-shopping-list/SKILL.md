---
name: gear-shopping-list
description: "Choose, price and check sport gear the user will buy"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: training.record
        description: "Where the training log lives: memory, a file path, or an app export"
        default: "memory"
---
# Gear Shopping List

Chooses, prices and checks the equipment a sport needs, for the user to buy. Good essentials make training safe and comfortable; gadgets do not. The coach never pays, orders or books.

## Trigger
The user needs equipment for a sport chosen or priced, asks from a shop whether an item is the right one, or asks for a gear check or how to care for what they own.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Web search or page fetch | current products, prices and availability | one search returns results |
| Image input, for a check from a photo | read the packaging the user photographed | the image opens |
| The training record, when `training.record` is a file | the gear inventory lives with it | the file opens |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Without web access, give the list without prices and say so: never quote a price you did not see. Try to open an image before saying you cannot see it.

## Configuration
`training.record`: the gear inventory (item; owned, to buy or bought; care rule) is kept beside the training log: in memory, in the file, or in the reply for the user to carry when the record is a read-only export. Set it with `hermes config set skills.config.training.record <value>`.

## Steps
1. Establish the sport and its conditions, from the record or by asking: where and in which season the user trains, how often, at what level.
2. Ask what the user already owns, and drop it from the list.
3. Ask for the sizing data that matters for each remaining need, in the user's own units, instead of guessing. [Examples by sport](references/examples-by-sport.md) show what to ask.
4. Start from the sport's safety items, then comfort. Leave gadgets out.
5. Choose one option per need, with the safety or comfort reason it matters. Where conditions decide the choice, give a budget option and an all-conditions option, and name your pick. For fit-critical items, recommend trying them on in a shop.
6. Check each item's current price and availability from a live source: product name, direct link, the price seen with its source and date, and whether the user's size is in stock. Add a total, and name every price you could not verify.
7. Hand over the list for the user to buy. Prefer one order from the user's usual shop: one delivery, easy returns.
8. For a check from a shop photo, read the packaging, not the shelf label. Answer yes or no first, then give the exact specification to look for.
9. Update the inventory: each item's status and its care rule, from [care rules](references/care-rules.md). Offer a periodic gear check.

## Decision rules
- The coach never buys: ordering, paying, booking and returning are the user's.
- One option per need, and a second only where conditions decide.
- Every item carries a safety or comfort reason. An item with neither is left out.
- Never guess a size: ask for the measurement, use the brand's own size chart, or send the user to try the item on.
- Never quote a price or stock from memory. When a shop puts a bot check in front of its pages, a search-result snippet may still show the current price: quote it with its date and ask the user to confirm on the site.
- A shelf label often belongs to the neighbouring item: the packaging decides.
- Safety items come first in the list and are not where a tight budget is saved.

## Done when
- The user has one list: an item per need with its reason, prices and availability with source and date, a total, and the unverified prices named.
- The inventory shows each item's status and care rule, and nothing was bought for the user.
