import datetime

import pytest

from helper import time_formatter, pace_formatter
from main import Run, TooManyArguments, count_args, NotEnoughArguments


def test_km_to_meter():
    for km in [1, 0, 100, 5.9287346, -69, 0.0001, -99.3]:
        run = Run(km=km, pace=datetime.timedelta(seconds=0))
        assert run.meters == km * 1000


def test_m_to_meter():
    for m in [1, 0, 100, 5.9287346, -609, 0.0001, -990.3]:
        run = Run(m=m, pace=datetime.timedelta(seconds=0))
        assert run.meters == m


def test_mile_to_meter():
    for mile in [1, 0, 100, 5.9287346, -609, 0.0001, -990.3]:
        run = Run(miles=mile, pace=datetime.timedelta(seconds=0))
        assert run.meters == mile * 1609.344


def test_set_time():
    run = Run(time=datetime.timedelta(hours=0, minutes=5, seconds=0), km=1)
    assert run.time == datetime.timedelta(hours=0, minutes=5, seconds=0)


def test_hours_to_seconds():
    run = Run(time=datetime.timedelta(hours=1, minutes=0, seconds=0), km=1)
    assert run.minutes == 60

    run = Run(time=datetime.timedelta(hours=0.5, minutes=0, seconds=0), km=1)
    assert run.minutes == 30

    run = Run(time=datetime.timedelta(hours=3, minutes=0, seconds=0), km=1)
    assert run.minutes == 60 * 3


def test_seconds_to_minutes():
    run = Run(time=datetime.timedelta(hours=0, minutes=0, seconds=600), km=1)
    assert run.minutes == 10
    assert run.time == datetime.timedelta(minutes=10)


def test_get_pace_from_time_and_distance():
    run = Run(time=datetime.timedelta(hours=1, minutes=0, seconds=0), km=12)
    assert run.pace == datetime.timedelta(minutes=5)

    run = Run(time=datetime.timedelta(hours=0, minutes=45, seconds=0), km=12)
    assert run.pace == datetime.timedelta(minutes=3, seconds=45)
    assert run.pace == datetime.timedelta(seconds=225)

    run = Run(time=datetime.timedelta(hours=0, minutes=100, seconds=0), miles=12)
    assert round(run.pace.total_seconds()) == datetime.timedelta(minutes=5, seconds=11).total_seconds()


def test_set_pace():
    p = datetime.timedelta(minutes=4, seconds=45)
    run = Run(pace=p, km=1)
    assert run.pace == p


def test_time_pace_to_distance():
    run = Run(time=datetime.timedelta(hours=1, minutes=0, seconds=0), pace=datetime.timedelta(minutes=5))
    assert run.meters == 12000

    run = Run(time=datetime.timedelta(hours=0, minutes=40, seconds=0), pace=datetime.timedelta(minutes=4, seconds=35))
    assert round(run.meters) == 8727

    run = Run(time=datetime.timedelta(hours=0, minutes=0, seconds=0), pace=datetime.timedelta(minutes=4, seconds=35))
    assert round(run.meters) == 0


def test_pace_distance_to_time():
    run = Run(meters=7844, pace=datetime.timedelta(minutes=4, seconds=35))
    assert round(run.time.total_seconds()) == 35 * 60 + 57

    run = Run(meters=0, pace=datetime.timedelta(minutes=5, seconds=1))
    assert round(run.time.total_seconds()) == 0


def test_count_none():
    assert count_args([None]) == 0
    assert count_args([]) == 0
    assert count_args([12, datetime.timedelta(seconds=2)]) == 2
    assert count_args([None, None, None]) == 0
    assert count_args([12, None, datetime.timedelta(seconds=2)]) == 2


def test_too_many_args():
    with pytest.raises(TooManyArguments):
        Run(meters=20, pace=datetime.timedelta(minutes=5, seconds=3), time=datetime.timedelta(hours=0, minutes=30, seconds=0))


def test_not_enough_args():
    with pytest.raises(NotEnoughArguments):
        Run(meters=20)
    with pytest.raises(NotEnoughArguments):
        Run(pace=datetime.timedelta(minutes=2))
    with pytest.raises(NotEnoughArguments):
        Run(hours=2, minutes=20)
    with pytest.raises(NotEnoughArguments):
        Run()


def test_time_formatter():
    d = time_formatter("1:45:21")
    assert d == datetime.timedelta(hours=1, minutes=45, seconds=21)

    d = time_formatter("45:21")
    assert d == datetime.timedelta(hours=0, minutes=45, seconds=21)

    d = time_formatter("5.5:21.5")
    assert d == datetime.timedelta(hours=0, minutes=5.5, seconds=21.5)

    d = time_formatter("1::50")
    assert d == datetime.timedelta(hours=1, minutes=0, seconds=50)
    assert d.total_seconds() == 60*60+50


def test_pace_formatter():
    assert pace_formatter(60) == "1m 0s"
    assert pace_formatter(3021) == "50m 21s"
    assert pace_formatter(3) == "3s"
    assert pace_formatter(2*60*60+23*60+24) == "2h 23m 24s"
    assert pace_formatter(60*60) == "1h 0m 0s"

def test_get_missing():
    run = Run(km=12, pace=datetime.timedelta(minutes=3, seconds=59))
    assert round(run.missing.total_seconds()) == 47*60 + 48

    run = Run(time=datetime.timedelta(minutes=60), pace=datetime.timedelta(minutes=4, seconds=44))
    assert round(run.missing) == 12676

    run = Run(time=datetime.timedelta(minutes=60), m=15000)
    assert run.missing == datetime.timedelta(minutes=4)

def test_get_missing_formatted():
    run = Run(km=12, pace=datetime.timedelta(minutes=3, seconds=59))
    assert run.missing_formatted() == "47m 48s"

    run = Run(time=datetime.timedelta(minutes=60), pace=datetime.timedelta(minutes=4, seconds=44))
    assert run.missing_formatted() == "12676 meters"

    run = Run(time=datetime.timedelta(minutes=60), m=15000)
    assert run.missing_formatted() == "4m 0s"

