import argparse
import logging
import sys

from webapp import create_app
from webapp.altravel_points import get_altravel_points
from webapp.autotravel_points import get_autotravel_points
from webapp.geocaching_points import get_geocaching_points


logging.basicConfig(
    level=logging.INFO, 
    filename="points_parsing.log", 
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
    )

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

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

app = create_app()
with app.app_context():
    if args.geo:
        logger.info("Parsing GEOCACHING only...")
        logger.info("GEOCACHING parser has been started!")
        get_geocaching_points()

    if args.alter:
        logger.info("Parse ALTERTRAVEL only...")
        logger.info("ALTERTRAVEL parser has been started!")
        get_altravel_points()

    if args.auto:
        logger.info("Parsing AUTOTRAVEL only...")
        logger.info("AUTOTRAVEL parser has been started!")
        get_autotravel_points()

    if len(sys.argv) <= 1:
        logger.info("Parsing ALL sources...")
        logger.info("GEOCACHING paser has been started!")
        get_geocaching_points()
        logger.info("ALTERTRAVEL paser has been started!")
        get_altravel_points()
        logger.info("AUTOTRAVEL paser has been started!")
        get_autotravel_points()
