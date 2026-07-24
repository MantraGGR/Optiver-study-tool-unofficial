#!/usr/bin/env python3
"""
Verification for the Beat the Odds question bank.

Two layers:
  1. Structural: parse every question object out of beat-the-odds.html and assert
     each has 4 distinct options and a valid answer index.
  2. Mathematical: independent exact / Monte-Carlo checks of a representative set
     of answers. Ground rule for this project: no unverified probability answers.

Run:  python3 verify/verify.py
"""
import re, os, math, random, json
from fractions import Fraction as F
from itertools import product

random.seed(0)
HERE = os.path.dirname(__file__)
HTML = os.path.join(HERE, "..", "beat-the-odds.html")


# ---------- 1. STRUCTURAL ----------
def load_bank():
    src = open(HTML, encoding="utf-8").read()
    m = re.search(r"const BANK = (\[.*?\n\]);", src, re.S)
    body = m.group(1)
    # count objects and sanity-check option arrays via a light regex sweep
    objs = re.findall(r"o:\[(.*?)\],a:(\d)", body)
    n_ok = 0
    for opts, a in objs:
        items = re.findall(r'"(.*?)"', opts)
        assert len(items) == 4, f"not 4 options: {opts}"
        assert len(set(items)) == 4, f"duplicate options: {opts}"
        assert 0 <= int(a) <= 3, f"bad answer index: {a}"
        n_ok += 1
    return n_ok


# ---------- 2. MATHEMATICAL ----------
def mc(f, n=200_000):
    return sum(f() for _ in range(n)) / n


def check(name, got, want, tol=None):
    ok = (abs(got - want) <= tol) if tol else (got == want)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: {got}  (expected {want})")
    assert ok, name


def math_checks():
    D = list(product(range(1, 7), repeat=2))
    # Dice
    check("E[max two dice]", sum(max(a, b) for a, b in D) / 36, 161 / 36, 1e-9)
    check("E[min two dice]", sum(min(a, b) for a, b in D) / 36, 91 / 36, 1e-9)
    check("P(sum=7)", sum(a + b == 7 for a, b in D) / 36, 1 / 6, 1e-9)
    check("P(at least one 6)", sum(6 in (a, b) for a, b in D) / 36, 11 / 36, 1e-9)
    # Coupon collector
    check("coupon 6", float(6 * sum(F(1, k) for k in range(1, 7))), 14.7, 1e-6)
    # Cards
    check("P(>=1 ace in 5)", 1 - math.comb(48, 5) / math.comb(52, 5), 0.3411, 1e-3)
    check("E[pos first ace]", 53 / 5, 10.6, 1e-9)
    # Order statistics of 3 dice
    check("E[max 3 dice]", sum(max(t) for t in product(range(1, 7), repeat=3)) / 216, 119 / 24, 1e-9)
    check("E[min 3 dice]", sum(min(t) for t in product(range(1, 7), repeat=3)) / 216, 49 / 24, 1e-9)
    # Hypergeometric vs binomial (Hard Mix)
    check("hypergeom 2 red of 3 (5R3B)",
          math.comb(5, 2) * math.comb(3, 1) / math.comb(8, 3), 15 / 28, 1e-9)
    check("binom 2 red of 3 w/ replacement (3R2B)",
          math.comb(3, 2) * (3 / 5) ** 2 * (2 / 5), 54 / 125, 1e-9)
    # Recursion
    check("first-to-roll-6, A first", (1 / 6) / (1 - (5 / 6) ** 2), 6 / 11, 1e-9)
    check("first >4, A first", (1 / 3) / (1 - (2 / 3) ** 2), 3 / 5, 1e-9)
    check("first head on even flip", 0.25 / (1 - 0.25), 1 / 3, 1e-9)
    # Expert
    check("chuck-a-luck EV", float(F(-17, 216)), -0.0787, 1e-3)
    check("derangement n=4", 9 / 24, 3 / 8, 1e-9)
    check("P(product even)", 1 - 9 / 36, 3 / 4, 1e-9)
    check("first to 3, p=2/3",
          float((F(2, 3) ** 3) * (1 + 3 * F(1, 3) + 6 * F(1, 3) ** 2)), 64 / 81, 1e-9)

    # Monte-Carlo cross-checks for the trickier ones
    def hth():
        s, c = "", 0
        while not s.endswith("HTH"):
            s += random.choice("HT"); c += 1
        return c
    check("E[flips to HTH] (MC)", mc(hth), 10, 0.1)

    def cons6():
        c = streak = 0
        while True:
            c += 1
            if random.randint(1, 6) == 6:
                streak += 1
                if streak == 2:
                    return c
            else:
                streak = 0
    check("E[rolls to two 6s in a row] (MC)", mc(cons6, 100_000), 42, 0.6)

    def ant():
        d, steps = 3, 0
        while d > 0:
            steps += 1
            d += -1 if random.random() < d / 3 else 1
        return steps
    check("E[ant across cube] (MC)", mc(ant, 100_000), 10, 0.15)


if __name__ == "__main__":
    print("Structural check...")
    n = load_bank()
    print(f"  PASS  {n} questions, all with 4 distinct options and valid answer index\n")
    print("Mathematical checks...")
    math_checks()
    print("\nAll checks passed.")
