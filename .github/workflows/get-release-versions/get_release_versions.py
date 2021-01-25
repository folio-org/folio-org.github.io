#!/usr/bin/env python3

# pylint: disable=C0413
import sys
if sys.version_info[0] < 3:
    raise RuntimeError("Python 3 or above is required.")

import argparse
import json
import logging
import os
import pprint
import sys

import requests
import github3

SCRIPT_VERSION = "1.0.0"

LOGLEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}
PROG_NAME = os.path.basename(sys.argv[0])
PROG_DESC = __import__('__main__').__doc__
LOG_FORMAT = "%(levelname)s: %(name)s: %(message)s"
logger = logging.getLogger(PROG_NAME)
logging.basicConfig(format=LOG_FORMAT)

def get_options():
    """Gets the command-line options."""
    parser = argparse.ArgumentParser(description=PROG_DESC)
    parser.add_argument(
        "-b", "--branch",
        required=True,
        help="Branch name of platform-complete."
    )
    parser.add_argument(
        "-l", "--loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Logging level. (Default: %(default)s)"
    )
    args = parser.parse_args()
    loglevel = LOGLEVELS.get(args.loglevel.lower(), logging.NOTSET)
    logger.setLevel(loglevel)

    # Display a version string
    logger.info("Using version: %s", SCRIPT_VERSION)
    return args.branch

def get_versions(branch):
    """Gets the configuration and assesses the versions."""
    url_config = "https://raw.githubusercontent.com/folio-org/platform-complete/{}/okapi-install.json".format(branch)
    exit_code = 0 # Continue processing to detect various issues, then return the result.
    try:
        http_response = requests.get(url_config)
        http_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.critical("HTTP error retrieving configuration file: %s", err)
        return 2
    except Exception as err:
        logger.critical("Error retrieving configuration file: %s", err)
        return 2
    else:
        logger.debug("Successfully retrieved configuration.")
        try:
            data = json.loads(http_response.text)
        except Exception as err:
            logger.error("Trouble loading JSON: %s", err)
            return 2
    for mod in data:
        print(mod['id'])
    return exit_code

def main():
    """Obtain okapi-install.json from platform-complete release branch and verify tags."""
    branch = get_options()
    exit_code = get_versions(branch)
    logging.shutdown()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
