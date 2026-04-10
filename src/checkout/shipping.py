from datetime import datetime, timedelta


def resolve_eta(zip_code, method="ground", holidays=None):
    if holidays is None:
        holidays = []
    base = 3
    if method == "ground":
        base = 5
    if zip_code.startswith("9"):
        base = base + 2
    for h in holidays:
        if h.weekday() == 5:
            base = base + 1
    eta = datetime.now() + timedelta(days=base)
    return eta.strftime("%Y-%m-%d")


def batch_zip_normalize(codes):
    out = []
    for c in codes:
        try:
            out.append(c.strip().upper())
        except (AttributeError, TypeError):
            out.append(c)
    return out
