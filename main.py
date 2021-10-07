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
        self.out = kwargs.get("out", "km")

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

    @property
    def pace_miles(self):
        pace = (self.time.total_seconds() * 1609.344) / self.meters
        return datetime.timedelta(seconds=pace)

    def _calc_pace(self):
        pace = (self.time.total_seconds() * 1000) / self.meters
        self.pace = datetime.timedelta(seconds=pace)

    def _calc_meters(self):
        self.meters = (self.time.total_seconds() / self.pace.total_seconds()) * 1000

    def _calc_time(self):
        self.time = datetime.timedelta(seconds=(self.meters / 1000) * self.pace.total_seconds())

    def overview(self):
        print("===== RUN =====")
        print(f"DISTANCE: {round(self.meters / 1000, 1)} KM")
        print(f"DISTANCE: {round(self.meters / 1609.344, 1)} Miles")
        print(f"TIME: {pace_formatter(self.time.total_seconds())}")
        print(f"PACE: {pace_formatter(self.pace.total_seconds())} per KM")
        print(f"PACE: {pace_formatter(self.pace_miles.total_seconds())} per Mile")

    @property
    def missing(self):
        if self.miss == 1:
            if self.out == "km":
                return round(self.meters / 1000, 1)
            if self.out == "miles":
                return round(self.meters / 1609.344, 1)
            return self.meters
        if self.miss == 2:
            return self.time
        else:
            if self.out == "miles":
                return self.pace_miles
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
