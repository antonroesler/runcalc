import datetime
from math import floor


def _pop_last(l):
    try:
        t = l.pop(-1)
        return t if t else 0
    except IndexError:
        return 0

def time_formatter(time: str):
    if time is None:
        return None
    units = time.split(":")
    s = _pop_last(units)
    m = _pop_last(units)
    h = _pop_last(units)
    return datetime.timedelta(hours=float(h), minutes=float(m), seconds=float(s))


def pace_formatter(seconds):
    seconds = floor(seconds)
    s = seconds % 60
    m = floor(seconds / 60)
    h = floor(m / 60)
    m = m % 60
    out = f"{s}s"
    if m or h:
        out = f"{m}m " + out
    if h:
        out = f"{h}h " + out
    return out