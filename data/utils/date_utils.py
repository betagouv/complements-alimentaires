from datetime import date


def diff_dates(d1: date, d2: date):
    """Return the delta between d1 and d2, in seconds."""
    return abs((d1 - d2).total_seconds())
