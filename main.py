import datetime

distances = {
    'm': 1,
    'meters': 1,
    'meter': 1,
    'km': 1000,
    'kilometer': 1000,
    'kilometers': 1000,
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
    t = datetime.timedelta(hours=h, minutes=m, seconds=s)
    return t if t.total_seconds() > 0 else None


def count_args(data):
    """
    Counts the number of elements in data that are not None
    :param data: list type
    :return: int
    """
    return sum(x is not None for x in data)


class Run:
    def __init__(self, **kwargs):
        self.meters: float = _get_meters(**kwargs)
        self.time: datetime.timedelta = _get_time(**kwargs)
        self.pace: datetime.timedelta = kwargs.get('pace')

        if count_args([self.meters, self.time, self.pace]) > 2:
            raise TooManyArguments
        if count_args([self.meters, self.time, self.pace]) < 2:
            raise NotEnoughArguments

        if self.meters is None:
            self._calc_meters()
        if self.time is None:
            self._calc_time()
        if self.pace is None:
            self._calc_pace()

    @property
    def minutes(self):
        return self.time.total_seconds() / 60

    def _calc_pace(self):
        sec = self.time.total_seconds()
        p_s_m = sec / self.meters
        pace = p_s_m * 1000
        self.pace = datetime.timedelta(seconds=pace)

    def _calc_meters(self):
        self.meters = (self.time.total_seconds() / self.pace.total_seconds()) * 1000

    def _calc_time(self):
        self.time = datetime.timedelta(seconds=(self.meters / 1000) * self.pace.total_seconds())


class TooManyArguments(Exception):
    """You must set exactly 2 of the 3 arguments [time, distance pace]"""


class NotEnoughArguments(Exception):
    """You must set exactly 2 of the 3 arguments [time, distance pace]"""
