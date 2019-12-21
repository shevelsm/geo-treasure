import argparse
import sys

from webapp.app import app
from webapp.geocahing_points import get_geocaching_points
from webapp.altravel_points import get_altravel_points


parser = argparse.ArgumentParser(description="Choose parsers to start")
parser.add_argument("-g", "--geo", default=False, help="run geocaching parser")
parser.add_argument("-a", "--alter", default=False, help="run altertravel parser")

args = parser.parse_args()

with app.app_context():
    if args.geo:
        get_geocaching_points()

    if args.alter:
        get_altravel_points()

    if not len(sys.argv) > 1:
        get_geocaching_points()
        get_altravel_points()
