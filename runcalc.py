import click

from helper import time_formatter, get_distance
from main import Run


@click.command()
@click.option('-d', help='Distance', default=None)
@click.option('-t', help='Time', default=None)
@click.option('-p', help='Pace', default=None)
@click.option('-o', help='Pace', default='km')
@click.option('-du', help='Unit of Distance, default m (meters), options are: miles, km', default='m')
@click.option('-l', help='Pace', is_flag=True)
def cli(d, t, du, p, l, o):
    t = time_formatter(t)
    p = time_formatter(p)
    if d:
        d, du = get_distance(d, du)
    kwargs = {du:d, 'time': t, 'pace': p, 'out': o}
    run = Run(**kwargs)
    if l:
        run.overview()
    else:
        print(run.missing_formatted())

if __name__ == '__main__':
    cli()