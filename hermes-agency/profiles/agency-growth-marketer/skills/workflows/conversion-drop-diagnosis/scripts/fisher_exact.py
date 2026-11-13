#!/usr/bin/env python3
"""Fisher exact test, two-sided, stdlib only.

Funnel volumes here are small (tens of conversions), so chi-square and eyeballed
percentage deltas both mislead. Use this before calling any before/after change real.

    python3 fisher_exact.py <succ_a> <n_a> <succ_b> <n_b>

Example -- a before/after that LOOKS like a 30% relative improvement:

    $ python3 fisher_exact.py 6 600 8 615
    A:      6/600    = 1.000%
    B:      8/615    = 1.301%
    two-sided p = 0.7895
    NOT significant at p<0.05 -- not a result yet.

"Not significant" is only "no effect" when each arm reached the sample size that
effect_size.py prints for the effect you care about. Below it, the verdict is
"cannot conclude, need X more days".
"""
import sys
from math import comb


def fisher_two_sided(a: int, n1: int, b: int, n2: int) -> float:
    """P(observing a table at least as extreme), successes a/n1 vs b/n2."""
    A, B, C, D = a, n1 - a, b, n2 - b
    if min(A, B, C, D) < 0:
        raise ValueError("successes cannot exceed totals")

    def p_table(w: int, x: int, y: int, z: int) -> float:
        return comb(w + x, w) * comb(y + z, y) / comb(w + x + y + z, w + y)

    observed = p_table(A, B, C, D)
    total = 0.0
    # enumerate every table with the same margins
    for i in range(0, min(A + B, A + C) + 1):
        j = (A + B) - i
        k = (A + C) - i
        l = (C + D) - k
        if j < 0 or k < 0 or l < 0:
            continue
        p = p_table(i, j, k, l)
        if p <= observed + 1e-12:
            total += p
    return min(total, 1.0)


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    a, n1, b, n2 = (int(x) for x in sys.argv[1:5])
    p = fisher_two_sided(a, n1, b, n2)
    print(f"A: {a:>5}/{n1:<6} = {100 * a / n1:.3f}%")
    print(f"B: {b:>5}/{n2:<6} = {100 * b / n2:.3f}%")
    print(f"two-sided p = {p:.4f}")
    if p < 0.05:
        print("significant at p<0.05 -- the change is real.")
    else:
        print("NOT significant at p<0.05 -- not a result yet. Check the sample size with")
        print("effect_size.py: below it, say 'cannot conclude', not 'no effect'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
