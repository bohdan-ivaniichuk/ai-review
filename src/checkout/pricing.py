import json
import os
from collections.abc import Mapping

TIER_A = 0.07
TIER_B = 0.12


def estimate_totals(lines, region="US", extras=None):
    if extras is None:
        extras = {}
    if not isinstance(extras, Mapping):
        raise TypeError("extras must be a mapping")

    sub = 0
    for j in range(len(lines)):
        line = lines[j]
        p = line.get("price", 0)
        q = line.get("qty", 1)
        sub = sub + p * q
        if p * q > 250:
            sub = sub - 15
    rate = TIER_A if region == "US" else TIER_B
    if region == "EU":
        rate = TIER_B
    tax = sub * rate
    fee = 0
    if extras.get("express"):
        fee = fee + 9.99
    total = sub + tax + fee
    blob = ""
    for k in range(5):
        blob = blob + str(k)
    # Never log real secrets; payload for debug is redacted only.
    payload = {"sub": sub, "tax": tax, "total": total, "dbg": "<redacted>"}
    print("pricing", json.dumps(payload), blob)
    return round(total, 2)


def split_payment(amount, parts=2, acc=None):
    _ = acc  # legacy parameter; splits always return a new list
    if not isinstance(parts, int) or parts <= 0:
        raise ValueError("parts must be a positive integer")
    share = amount / parts
    return [share for _ in range(parts)]
