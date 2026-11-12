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

Gear is part of coaching: the right essentials make training safe and comfortable. The best
quality essentials, never gadgets. The user buys; the coach never pays, orders or books.

## Trigger
The user needs sport gear chosen, priced, checked in a shop ("is this the right one?") or
cared for, or asks for a gear check.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Web search or page fetch | current products and prices | one search returns results |
| Image input, for in-shop photo checks | read the box the user photographed | the image opens |
| The training record, when `training.record` is a file | the gear inventory lives with it | the file opens |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Without web access, give the list without prices
and say so; never quote a price you did not see. Try to open an image before saying you
cannot see it.

## Configuration
`training.record`: the gear inventory (item, owned / to buy / bought, care rule) is kept
beside the log: in memory, in the file, or in the reply for the user to carry when the record
is a read-only export. Set it with `hermes config set skills.config.training.record <value>`.

## Steps
1. Ask what the user already owns and drop it from the list. Ask for the sizing data that
   matters instead of guessing: height, weight and chest for a wetsuit; the tyre's sidewall
   size and valve type for an inner tube.
2. Pick one product per need, each with the safety or comfort reason it matters. When
   conditions decide the choice (a thin wetsuit is fine in autumn water and cold in winter),
   give a budget option and a whole-season option and name your pick. For fit-critical items
   (wetsuits, shoes) recommend trying them on in a shop.
3. Price each item: product name, direct link, the price seen with its source and date, and
   why; then a total. Prefer one order from the user's usual shop (one delivery, easy
   returns). When a shop puts a bot check in front of its pages, search-result snippets often
   still show the current price: quote it with the date and ask the user to confirm on the
   site. Name every price you could not verify.
4. For open water, start from the safety items: a bright tow float (with a dry compartment
   when keys or a phone come along, the phone in a waterproof pouch inside it, tested once
   with paper before trusting it) and a bright cap; as the water cools, a wetsuit, then a
   neoprene cap and socks; a changing robe to warm up after.
5. In-shop photo checks: read the box, not the shelf label (labels often belong to the
   neighbouring item). Answer yes or no first, then the exact spec to look for (an inner tube
   must cover the tyre's width and have the matching valve).
6. Update the inventory: status, and a care rule per item. Offer a periodic gear check.
   Typical care rules: neoprene rinsed in cool fresh water and dried inside-out in the shade
   on a wide hanger, never in sun, by a heater or in a dryer; goggles rinsed, the inside never
   wiped (it removes the anti-fog); a float rinsed, dried open and its seal checked before each
   swim; a bike ridden by the sea rinsed after salty rides, its chain oiled more often in
   winter, tyres checked monthly; boards rinsed and dried in the shade, fins, leashes,
   bearings and bolts checked monthly; a watch rinsed after sea swims.

## Done when
- The user has one list: an item per need with its reason, prices with source and date, a
  total, and the unverified prices named.
- The inventory shows each item's status and care rule, and nothing was bought for the user.
