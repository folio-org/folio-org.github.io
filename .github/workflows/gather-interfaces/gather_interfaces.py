#!/usr/bin/env python3

"""
Gather current interfaces from the ModuleDescriptor Registry.
"""

import argparse
import json
import logging
from pathlib import Path
import sys
import urllib.error
import urllib.request

SCRIPT_VERSION = "1.0.0"

LOGLEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

PROG_NAME = Path(sys.argv[0]).name
PROG_PATH = Path(__file__).absolute().parent
PROG_DESC = __import__("__main__").__doc__
LOG_FORMAT = "%(levelname)s: %(name)s: %(message)s"
LOGGER = logging.getLogger(PROG_NAME)


def get_options():
    """
    Gets the command-line options.
    Verifies configuration.
    """
    parser = argparse.ArgumentParser(description=PROG_DESC)
    parser.add_argument(
        "-o",
        "--output-file",
        default="interfaces.jsonl",
        help="Pathname to output JSONL file. (Default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level. (Default: %(default)s)",
    )
    args = parser.parse_args()
    logging.basicConfig(format=LOG_FORMAT)
    if args.loglevel:
        loglevel = LOGLEVELS.get(args.loglevel.lower(), logging.NOTSET)
        LOGGER.setLevel(loglevel)
    return args.output_file


def get_mds():
    """
    Gets the latest ModuleDescriptors.
    """
    content = []
    headers = {
        "user-agent": f"{PROG_NAME}/{SCRIPT_VERSION}",
        "content-type": "application/json",
        "accept": "application/json",
    }
    url_registry = (
        "https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&full=true"
    )
    req = urllib.request.Request(url_registry, headers=headers)
    try:
        response = urllib.request.urlopen(req)  # pylint: disable=R1732
    except urllib.error.HTTPError as error:
        LOGGER.critical("HTTPError: %s %s", error.status, error.reason)
        sys.exit(1)
    except urllib.error.URLError as error:
        LOGGER.critical("URLError: %s", error.reason)
        sys.exit(1)
    else:
        data = response.read()
        content = json.loads(data.decode("utf-8"))
    return content


def get_interfaces(module_descriptor, section):
    """
    Extracts the interfaces id,version from the MD section.
    """
    section_details = []
    try:
        interfaces = module_descriptor[section]
    except KeyError:
        pass
    else:
        for interface in interfaces:
            detail = f"{interface['id']} {interface['version']}"
            section_details.append(detail)
    return sorted(section_details)


def parse_mds(mds_json):
    """
    Parses the set of ModuleDescriptors to obtain the interfaces:
    provided, required, optional.
    """
    details = []
    sections = ["provides", "requires", "optional"]
    for module_descriptor in mds_json:
        json_packet = {}
        try:
            json_packet["id"] = module_descriptor["id"]
        except KeyError:
            pass
        else:
            json_packet["id"] = module_descriptor["id"]
        for section in sections:
            json_packet[section] = get_interfaces(module_descriptor, section)
        details.append(json_packet)
    return details


def store_output(output_pn, details):
    """
    Stores the output as compact JSON.
    """
    LOGGER.info("Storing output: %s", output_pn)
    with open(output_pn, mode="w", encoding="utf-8") as output_fh:
        for item in details:
            output_fh.write(json.dumps(item, sort_keys=True, indent=None) + "\n")


def main():
    """
    Gather current interfaces from the ModuleDescriptor Registry.

    Returns:
        token
    Exit values:
        0: Success.
        1: One or more failures with processing.
        2: Configuration issues.
    """
    exit_code = 0
    output_pn = get_options()
    mds_json = get_mds()
    details = parse_mds(mds_json)
    store_output(output_pn, details)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
