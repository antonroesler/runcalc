import datetime

import pytest

from main import Run


def test_km_to_meter():
    for km in [1, 0, 100, 5.9287346, -69, 0.0001, -99.3]:
        run = Run(km=km)
        assert run.meters == km * 1000


def test_m_to_meter():
    for m in [1, 0, 100, 5.9287346, -609, 0.0001, -990.3]:
        run = Run(m=m)
        assert run.meters == m


def test_mile_to_meter():
    for mile in [1, 0, 100, 5.9287346, -609, 0.0001, -990.3]:
        run = Run(miles=mile)
        assert run.meters == mile * 1609.344


def test_set_time():
    run = Run(minutes=5)
    assert run.time == datetime.timedelta(hours=0, minutes=5, seconds=0)


def test_hours_to_seconds():
    run = Run(hours=1)
    assert run.minutes == 60

    run = Run(hours=0.5)
    assert run.minutes == 30

    run = Run(hours=3)
    assert run.minutes == 60 * 3


def test_seconds_to_minutes():
    run = Run(seconds=600)
    assert run.minutes == 10
    assert run.time == datetime.timedelta(minutes=10)


def test_get_pace_from_time_and_distance():
    run = Run(hours=1, km=12)
    assert run.pace == datetime.timedelta(minutes=5)

    run = Run(minutes=45, km=12)
    assert run.pace == datetime.timedelta(minutes=3, seconds=45)
    assert run.pace == datetime.timedelta(seconds=225)

    run = Run(minutes=100, miles=12)
    assert round(run.pace.total_seconds()) == datetime.timedelta(minutes=5, seconds=11).total_seconds()
