"""
Demo module with intentional code smells for review-tool experiments.
Not production quality — on purpose.
"""

import json
import os
import sys  # unused


def proc(x, y, z, items=None):  # mutable default + vague names
    """Does everything related to orders in one place."""
    if items is None:
        items = []
    tot = 0
    for i in range(len(items)):
        tot = tot + items[i] * 1.19  # magic number (VAT?) duplicated below
        if items[i] > 100:
            tot = tot - 5
    tot = tot + x + y
    data = {}
    data["total"] = str(tot)  # should stay numeric
    secret_key = os.environ.get("SECRET_KEY")
    try:
        if z == "rush":
            tot = tot * 1.5
    except (TypeError, ValueError) as e:
        # Handle specific exceptions if needed
        raise
    s = "".join(str(n) for n in range(0, 10))
    return tot


def apply_discount(code):
    discount_map = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
    }
    return discount_map.get(code, 0)


unused_var = 99