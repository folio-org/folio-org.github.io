#!/usr/bin/env python3

# pylint: disable=C0413
import sys
if sys.version_info[0] < 3:
    raise RuntimeError("Python 3 or above is required.")

import argparse
import json
import logging
from operator import itemgetter
import os
import pprint
import re
import sys
from time import sleep

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
    delay = 5 # sleep between api requests
    exit_code = 0 # Continue processing to detect various issues, then return the result.
    repos_count = 0
    repos_json = {}
    repos_json["metadata"] = {}
    repos_json["metadata"]["branch"] = branch
    repos_json["repos"] = []
    mod_re = re.compile(r"^(.+)-([0-9.]+)$")
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
    token_name = "ALL_REPOS_READ_ONLY"
    token = os.environ.get(token_name)
    if not token:
        logger.critical("Missing environment: %s", token_name)
        return 2
    else:
        github = github3.login(token=token)
    for mod in sorted(data, key=itemgetter('id')):
        repos_count += 1
        match = re.search(mod_re, mod['id'])
        if match:
            mod_name = match.group(1)
            mod_version = match.group(2)
            logger.debug("%s %s", mod_name, mod_version)
        else:
            logger.error("Could not determine module version: %s", mod['id'])
            exit_code = 1
            continue
        repos_json_packet = {}
        repos_json_packet['name'] = mod_name
        tag_name = "v" + mod_version
        flag_tag_found = False
        repo_short = github.repository("folio-org", mod_name)
        tags = repo_short.tags(10)
        for tag in tags:
            logger.debug("  tag_name=%s sha=%s", tag.name, tag.commit.sha)
            if tag_name in tag.name:
                release_obj = repo_short.release_from_tag(tag.name)
                logger.debug("  release_name=%s published_at=%s target_commitish=%s", release_obj.name, release_obj.published_at, release_obj.target_commitish)
                repos_json_packet['releaseTag'] = tag.name
                repos_json_packet['releaseName'] = release_obj.name
                release_date = release_obj.published_at.isoformat(sep='T')
                repos_json_packet['releaseDate'] = release_date
                repos_json_packet['releaseTarget'] = release_obj.target_commitish
                flag_tag_found = True
                break
        if not flag_tag_found:
            logger.error("Could not determine release tag: %s", mod['id'])
            exit_code = 1
        repos_json['repos'].append(repos_json_packet)
        # FIXME: testing
        if repos_count == 4:
            break
        logger.debug("Sleeping %s seconds", delay)
        sleep(delay)
    logger.debug("Assessed %s repos.", repos_count)
    return exit_code, repos_json

def main():
    """Obtain okapi-install.json from platform-complete release branch and verify tags."""
    branch = get_options()
    (exit_code, repos_json) = get_versions(branch)
    os.makedirs("_data", exist_ok=True)
    output_pn = os.path.join("_data", "releases-backend-{}.json".format(branch))
    with open(output_pn, "w") as output_fh:
        output_fh.write(json.dumps(repos_json, sort_keys=True, indent=2, separators=(",", ": ")))
        output_fh.write("\n")
    logging.shutdown()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
