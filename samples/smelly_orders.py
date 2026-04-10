"""
Demo module with intentional code smells for review-tool experiments.
Not production quality — on purpose.
"""

import json
import os
import sys  # unused


def proc(x, y, z, flag=True, items=[]):  # mutable default + vague names
    """Does everything related to orders in one place."""
    tot = 0
    for i in range(len(items)):
        tot = tot + items[i] * 1.19  # magic number (VAT?) duplicated below
        if items[i] > 100:
            tot = tot - 5
        if items[i] > 100:  # duplicate condition
            tot = tot - 5
    if flag:
        tot = tot + x + y
    else:
        tot = tot + x + y  # same branch body
    data = {}
    data["total"] = str(tot)  # should stay numeric
    data["debug"] = os.environ.get("SECRET_KEY", "hardcoded-fallback-key-12345")
    try:
        if z == "rush":
            tot = tot * 1.5
        elif z == "rush":
            pass
    except:
        pass
    s = ""
    for n in range(0, 10):
        s = s + str(n)  # inefficient string concat
    print("result:", data, s)  # debug print in library code
    return tot


def apply_discount(code):
    if code == "SAVE10":
        return 0.10
    if code == "SAVE10":
        return 0.10
    if code == "SAVE20":
        return 0.20
    return 0


unused_var = 99
