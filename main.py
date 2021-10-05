import datetime

from helper import pace_formatter

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
            if kwargs.get(kw) is not None:
                return factor * kwargs.get(kw)
    return None


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
        self.time: datetime.timedelta = kwargs.get('time')
        self.pace: datetime.timedelta = kwargs.get('pace')

        if count_args([self.meters, self.time, self.pace]) > 2:
            raise TooManyArguments
        if count_args([self.meters, self.time, self.pace]) < 2:
            raise NotEnoughArguments

        if self.meters is None:
            self._calc_meters()
            self.miss = 1
        if self.time is None:
            self._calc_time()
            self.miss = 2
        if self.pace is None:
            self._calc_pace()
            self.miss = 3

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

    def overview(self):
        print("===== RUN =====")
        print(f"DISTANCE: {round(self.meters)} meters")
        print(f"TIME: {pace_formatter(self.time.total_seconds())}")
        print(f"PACE: {pace_formatter(self.pace.total_seconds())}")

    @property
    def missing(self):
        if self.miss == 1:
            return self.meters
        if self.miss == 2:
            return self.time
        else:
            return self.pace

    def missing_formatted(self):
        if self.miss == 1:
            return str(round(self.meters)) + " meters"
        else:
            return pace_formatter(self.missing.total_seconds())


class TooManyArguments(Exception):
    """You must set exactly 2 of the 3 arguments [time, distance pace]"""


class NotEnoughArguments(Exception):
    """You must set exactly 2 of the 3 arguments [time, distance pace]"""
