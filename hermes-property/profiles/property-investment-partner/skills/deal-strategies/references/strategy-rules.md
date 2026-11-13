# Strategy rules

## Working order

Market and profitability → rejection if the margin is insufficient → planning
→ tax, financing, offer. A property is ruled out **only after** divisions,
partial sales and mixed structures have been tested.

## Rules

- **The right structure for the area.** If the investor file reserves an area
  for certain strategies, a strategy outside its area is flagged, not
  proposed.
- **A threshold is read in the investor file.** A margin threshold the
  investor mentioned without recording it is presented as such and confirmed
  before a deal is ruled out on it.
- **Two rules pointing in opposite directions are not confused.** An entry
  discount on the asking price and a resale premium apply to two different
  bases; mixing them distorts the ceiling price both ways.
- **A purchase option is a different regime, not a cheaper purchase.**
  Acquisition costs apply to what is bought, not to the full price of a deal
  where part stays under option. The duties on a structure under option depend
  on its drafting and on who finally buys: present them as scenarios, with
  conditions checked by `property-accountant-be` and `property-notary`.
  Applying them wrongly rejects a good deal; omitting them wrongly accepts a
  bad one.
- **Impossible is not risky.** When a condition is missing (unrecognized unit,
  short-term letting prohibited), the strategy comes out "impossible", with
  the reason, not "risky".
- **A rental is not dressed up as a resale.** A rental deal is judged on its
  cash flow and yield, not on a resale ceiling price.
- **A discount must be explained.** If the property is below market, say why;
  if it is because of works the investor does at cost price, that is the
  investor's ground. Otherwise, look for what the market knows and you do not.
- **Corporate tax follows the investor's rule**, when the investor acts
  through a company. The investor file says whether a deal is judged before or
  after tax; without it, cost before tax and say so.
- **Shared housing** is tested only where demand is shown, **short-term
  letting** only if it can be authorized.
- **A good deal holds in the safety scenario.**

## Who supplies what

- The works budget: `property-works-estimator`, **always**; this profile never
  costs the works itself.
- How many units are recognized: `property-architect`; without it, neither
  option nor division.
- Duties, VAT, tax: `property-accountant-be` / `property-accountant-fr`.
- Auction conditions, co-ownership, basic deed: `property-notary`.
- What a clause means, a running lease: `property-lawyer`.
