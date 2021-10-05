from setuptools import setup

setup(
    name='runcalc',
    version='0.1',
    py_modules=['runcalc'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        runcalc=runcalc:cli
    ''',
)