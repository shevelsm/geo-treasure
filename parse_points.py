import argparse
import sys

from webapp.app import app
from webapp.altravel_points import get_altravel_points
from webapp.autotravel_points import get_autotravel_points
from webapp.geocaching_points import get_geocaching_points


parser = argparse.ArgumentParser(description="Choose parsers to start")
parser.add_argument(
    "--alter", default=False, nargs="?", const=True, help="run altertravel parser",
)
parser.add_argument(
    "--auto", default=False, nargs="?", const=True, help="run autotravel parser",
)
parser.add_argument(
    "--geo", default=False, nargs="?", const=True, help="run geocaching parser",
)

args = parser.parse_args()

with app.app_context():
    if args.geo:
        get_geocaching_points()

    if args.alter:
        get_altravel_points()

    if args.auto:
        get_autotravel_points()

    if len(sys.argv) <= 1:
        get_geocaching_points()
        get_altravel_points()
        get_autotravel_points()
