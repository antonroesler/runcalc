import datetime

distances = {
    'm': 1,
    'km': 1000,
    'miles': 1609.344
}


def _get_meters(**kwargs):
    for kw in kwargs:
        if factor := distances.get(kw):
            return factor * kwargs.get(kw)
    return None


def _get_time(**kwargs):
    h = kwargs.get('hours', 0)
    m = kwargs.get('minutes', 0)
    s = kwargs.get('seconds', 0)
    return datetime.timedelta(hours=h, minutes=m, seconds=s)


class Run:
    def __init__(self, **kwargs):
        self._meters: float = _get_meters(**kwargs)
        self.time: datetime.timedelta = _get_time(**kwargs)

    @property
    def meters(self):
        return self._meters

    @property
    def minutes(self):
        return self.time.total_seconds() / 60


    @property
    def pace(self):
        sec = self.time.total_seconds()
        p_s_m = sec/self._meters
        pace = p_s_m * 1000
        return datetime.timedelta(seconds=pace)