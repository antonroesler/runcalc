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

distances = {
    'marathon': 42194.988,
    'full': 42194.988,
    'half': 21097.494,
    'half-marathon': 21097.494,
    '10k': 10000,
    '5k': 5000,
    '10K': 10000,
    '5K': 5000,
    '1M': 1609.344
}
def get_distance(distance: str, distance_unit: str):
    if distance.isnumeric():
        return float(distance), distance_unit
    d = distances.get(distance)
    if not d:
        raise ValueError(f"{distance} is not a valid distance.")
    return distances[distance], 'm'