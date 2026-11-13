#!/usr/bin/env python3
"""Fisher exact p + 80%-power sample sizing for low-volume funnel comparisons.

Stdlib only (math.comb) - scipy is not needed and is often unavailable.

Use BEFORE reporting an A/B or before/after funnel delta as a result, and before
agreeing to a verification date: at a ~1% baseline and a few dozen sessions/day,
detecting even a 2x improvement takes weeks per arm. An underpowered check returns
"flat" by construction and gets misread as the fix having failed.

  python effect_size.py --before 3 150 --after 2 120 \\
                        --baseline 0.02 --target 0.04 --per-day 40

  --before/--after  successes total   (e.g. form-views, sessions)
  --baseline        current rate to power against (default: before rate)
  --target          rate worth detecting (default: 2x baseline)
  --per-day         sessions/day in the arm, to convert N into calendar days
"""
import argparse
import math


def fisher_exact_two_tailed(a, b, c, d):
    """Two-tailed Fisher exact p for the 2x2 table [[a, b], [c, d]].

    Sums the hypergeometric probability of every table at least as extreme as
    the observed one, holding both margins fixed.
    """
    n = a + b + c + d
    if n == 0:
        return 1.0
    row1, col1 = a + b, a + c

    def prob(x):
        # table (x, row1-x, col1-x, n-row1-col1+x)
        return (math.comb(row1, x) * math.comb(n - row1, col1 - x)) / math.comb(n, col1)

    observed = prob(a)
    lo = max(0, col1 - (n - row1))
    hi = min(row1, col1)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed + 1e-12))


def sessions_per_arm(p1, p2, power=0.80, alpha=0.05):
    """Two-proportion z-test sample size per arm (two-tailed)."""
    z_alpha = 1.959964  # two-tailed 0.05
    z_beta = {0.80: 0.841621, 0.90: 1.281552}.get(power, 0.841621)
    if p1 == p2:
        return float("inf")
    pbar = (p1 + p2) / 2
    num = (z_alpha * math.sqrt(2 * pbar * (1 - pbar))
           + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / ((p2 - p1) ** 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", nargs=2, type=int, metavar=("SUCC", "TOTAL"), required=True)
    ap.add_argument("--after", nargs=2, type=int, metavar=("SUCC", "TOTAL"), required=True)
    ap.add_argument("--baseline", type=float)
    ap.add_argument("--target", type=float)
    ap.add_argument("--per-day", type=float)
    ap.add_argument("--power", type=float, default=0.80)
    args = ap.parse_args()

    bs, bt = args.before
    as_, at = args.after
    rb = bs / bt if bt else 0.0
    ra = as_ / at if at else 0.0

    print(f"before: {bs}/{bt} = {rb * 100:.2f}%")
    print(f"after : {as_}/{at} = {ra * 100:.2f}%")

    p = fisher_exact_two_tailed(bs, bt - bs, as_, at - as_)
    print(f"Fisher exact (two-tailed) p = {p:.3f}"
          f"{'  -> NOT significant; do not report as a result' if p > 0.05 else ''}")

    baseline = args.baseline if args.baseline is not None else (rb or 0.01)
    target = args.target if args.target is not None else baseline * 2
    n = sessions_per_arm(baseline, target, power=args.power)
    print(f"\nto detect {baseline * 100:.2f}% -> {target * 100:.2f}% "
          f"at {args.power * 100:.0f}% power, alpha 0.05:")
    print(f"  {n} sessions PER ARM")
    if args.per_day:
        print(f"  at {args.per_day:g} sessions/day = {math.ceil(n / args.per_day)} days per arm")
        print("  -> any verification scheduled sooner than this returns 'flat' by construction")


if __name__ == "__main__":
    main()
