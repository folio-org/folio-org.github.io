#!/usr/bin/env python3

"""
Gather schema changes for backend modules in platform-complete release branch
and compare with current development.

   Returns:
       0: Success.
       1: One or more failures with processing.
       2: Configuration issues.
"""

# pylint: disable=C0413
import sys
if sys.version_info[0] < 3:
    raise RuntimeError("Python 3 or above is required.")

import argparse
import datetime
import fnmatch
import json
import logging
import os
from shutil import make_archive
from shutil import move
from shutil import copytree
from time import sleep
from werkzeug.utils import secure_filename
import tempfile

import requests
import sh
import yaml

SCRIPT_VERSION = "1.3.0"

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

    # Ensure that commands are available
    bin_extra_dirs = "/home/linuxbrew/.linuxbrew/bin"
    if not sh.which("jd", bin_extra_dirs):
        logger.critical("'jd' is not available.")
        sys.exit(2)
    return args.branch

def get_config_data(url):
    """Gets the specified data file."""
    try:
        http_response = requests.get(url)
        http_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.critical("HTTP error retrieving configuration file: %s", err)
        sys.exit(1)
    except Exception as err:
        logger.critical("Error retrieving configuration file: %s", err)
        sys.exit(1)
    else:
        logger.debug("Successfully retrieved configuration.")
        try:
            data = json.loads(http_response.text)
        except Exception as err:
            logger.error("Trouble loading JSON: %s", err)
            sys.exit(1)
    return data

def get_url_contents(url):
    """Gets the file contents."""
    status = True
    contents = ""
    try:
        http_response = requests.get(url)
        http_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.critical("HTTP error retrieving file: %s", err)
        status = False
    except Exception as err:
        logger.critical("Error retrieving file: %s", err)
        status = False
    else:
        contents = json.loads(http_response.text)
    return status, contents

def validate_filename(filename):
    "Returns filename if it is valid on all operating systems, otherwise raises ValueError"
    cleaned_filename = secure_filename(filename)
    if cleaned_filename == filename:
        return cleaned_filename
    raise ValueError('Invalid filename: "{}", valid filename: "{}"'.format(filename, cleaned_filename))

def validate_filepath(filepath):
    "Returns filepath if it is valid on all operating system, otherwises raises ValueError"
    cleaned_filepath = '/'.join(secure_filename(filename) for filename in filepath.split('/'))
    if cleaned_filepath == filepath:
        return cleaned_filepath
    raise ValueError('Invalid filepath: "{}", valid filepath: "{}"'.format(filepath, cleaned_filepath))

def get_repo_details(repos, repo_name):
    """Gets the details for the specified repository."""
    repo_details = {}
    for repo in repos['repos']:
        if repo['name'] == repo_name:
            repo_details = repo
            break
    return repo_details

def configure_excludes():
    """Configure the excluded directories and excluded files."""
    # FIXME: If apiExcludes in module's Jenkinsfile, then exclude them too
    exclude_dirs_list = ["raml-util", "raml-storage", "acq-models",
        "rtypes", "traits", "bindings", "examples", "_examples"
        "node_modules", ".git"]
    exclude_files = []
    exclude_dirs = set(exclude_dirs_list)
    #logger.debug("Excluding directories for os.walk: %s", exclude_dirs)
    return exclude_dirs, exclude_files

def construct_raml_include(loader, node):
    "Add a special construct for YAML loader"
    return loader.construct_yaml_str(node)

def prepare_s3_publish(branch):
    """Prepares the generated files for publish to S3.
    A Github workflow action follows to do the actual publish.
    """
    status = True
    input_dir = "schemadiff"
    zip_base_pn = "schema-diff-{}".format(branch)
    zip_pn = make_archive(zip_base_pn, "zip", input_dir)
    move(zip_pn, os.path.join(input_dir, branch))
    return status

def do_jd(file_1_pn, file_2_pn):
    """Compare the JSON files using 'jd'
    exit values: 0=same 1=diff 2=exception
    """
    status = True
    result = ""
    try:
        result = sh.jd(file_1_pn, file_2_pn, _ok_code=[0,1]).stdout.decode().strip()
    except sh.ErrorReturnCode as err:
        logger.error("Trouble doing jd: %s", err.stderr.decode())
        status = False
    return status, result

def show_api_diff(repo_name, mod_name, version, release_sha, api_directory, branch):
    """Show API schema differences.
    Clones the repo mainline and release to temporary directories.
    Compares each between release and mainline.
    """
    status = True
    errors = []
    files = []
    output_dir = os.path.abspath(os.path.join("schemadiff", branch, mod_name))
    output_api_dir = os.path.join(output_dir, "api")
    os.makedirs(output_api_dir, exist_ok=True)
    url_git = "https://github.com/folio-org/{}".format(repo_name)
    with tempfile.TemporaryDirectory(suffix='tmp') as temp_dir_1:
        release_dir = os.path.join(temp_dir_1, repo_name)
        release_api_dir = os.path.join(release_dir, api_directory)
        try:
            sh.git.clone("--recursive", url_git, _cwd=temp_dir_1)
        except sh.ErrorReturnCode as err:
            msg = "Trouble doing git clone"
            logger.critical("%s: %s: %s", repo_name, msg, err.stderr.decode())
            status = False
            errors.append(msg)
            return status, errors, files
        else:
            with tempfile.TemporaryDirectory(suffix='tmp') as temp_dir_2:
                # validate_pathname prevents path traversal vulnerability.
                # Security scanners like snyk.io notice that json_versions is fetched from a URL
                # and therefore is external (=dangerous) data.
                # CWE-23: https://cwe.mitre.org/data/definitions/23.html
                main_dir = validate_filepath(os.path.join(temp_dir_2, repo_name))
                main_api_dir = validate_filepath(os.path.join(main_dir, api_directory))
                copytree(release_dir, main_dir)
                try:
                    sh.git.checkout(release_sha, _cwd=release_dir)
                except sh.ErrorReturnCode as err:
                    msg = "Trouble doing git checkout release_sha"
                    logger.critical("%s: %s: %s", repo_name, msg, err.stderr.decode())
                    status = False
                    errors.append(msg)
                    return status, errors, files
                else:
                    try:
                        sh.git.submodule.update("--init", "--recursive", _cwd=release_dir)
                    except sh.ErrorReturnCode as err:
                        msg = "Trouble doing git submodule update"
                        logger.critical("%s: %s: %s", repo_name, msg, err.stderr.decode())
                        status = False
                        errors.append(msg)
                        return status, errors, files
                    else:
                        (exclude_dirs, exclude_files) = configure_excludes()
                        schemas_release = find_api_schemas(release_api_dir, exclude_dirs, exclude_files)
                        schemas_main = find_api_schemas(main_api_dir, exclude_dirs, exclude_files)
                        (schemas_common, schemas_old, schemas_new) = list_common_schemas(
                            release_api_dir, main_api_dir, schemas_release, schemas_main)
                        files_list = process_api_schemas(
                            schemas_common, release_api_dir, main_api_dir, output_dir, version)
                        files.extend(files_list)
                        if schemas_old:
                            for schema_fn in schemas_old:
                                file_record = {}
                                file_record['fileName'] = schema_fn
                                file_record['state'] = 'removed'
                                files.append(file_record)
                        if schemas_new:
                            for schema_fn in schemas_new:
                                file_record = {}
                                file_record['fileName'] = schema_fn
                                file_record['state'] = 'added'
                                files.append(file_record)
                        schemas_parent_release = find_api_schemas_parent(release_api_dir, exclude_dirs, exclude_files)
                        schemas_parent_main = find_api_schemas_parent(main_api_dir, exclude_dirs, exclude_files)
                        (schemas_common, schemas_old, schemas_new) = list_common_schemas(
                            release_api_dir, main_api_dir, schemas_parent_release, schemas_parent_main)
                        dereference_schemas(schemas_common, release_api_dir, main_api_dir)
                        files_list = process_api_parent_schemas(
                            schemas_common, release_api_dir, main_api_dir, output_dir, version)
                        files.extend(files_list)
                        if schemas_old:
                            for schema_fn in schemas_old:
                                file_record = {}
                                file_record['fileName'] = os.path.join("parents", schema_fn)
                                file_record['state'] = 'removed'
                                files.append(file_record)
                        if schemas_new:
                            for schema_fn in schemas_new:
                                file_record = {}
                                file_record['fileName'] = os.path.join("parents", schema_fn)
                                file_record['state'] = 'added'
                                files.append(file_record)
    return status, errors, files

def find_api_schemas(api_dir, exclude_dirs, exclude_files):
    """Locate the list of relevant schemas."""
    schema_files = []
    for root, dirs, files in os.walk(api_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for extension in ["*.json", "*.schema"]:
            for schema_fn in fnmatch.filter(files, extension):
                if not schema_fn in exclude_files:
                    schema_files.append(os.path.join(root, schema_fn))
    return sorted(schema_files)

def find_api_schemas_parent(api_dir, exclude_dirs, exclude_files):
    """Locate the list of relevant parent schemas.
    These are declared in the api description files.
    """
    api_files = []
    schema_files = set()
    for root, dirs, files in os.walk(api_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for extension in ["*.raml"]:
            for api_fn in fnmatch.filter(files, extension):
                if not api_fn in exclude_files:
                    api_files.append(os.path.join(root, api_fn))
    # get the declared RAML "types"
    for api_fn in api_files:
        api_subdir = os.path.split(os.path.relpath(api_fn, start=api_dir))[0]
        with open(api_fn) as input_fh:
            try:
                content = yaml.safe_load(input_fh)
            except yaml.YAMLError as err:
                logger.critical("Trouble parsing as YAML file '%s': %s", api_fn, err)
            else:
                try:
                    types = content["types"]
                except KeyError:
                    pass
                else:
                    for decl in types:
                        type_fn = types[decl]
                        if isinstance(type_fn, str):
                            type_pn = os.path.normpath(os.path.join(api_dir, api_subdir, type_fn))
                            # The "types" can be other than schema.
                            file_extension = os.path.splitext(type_pn)[1]
                            if not file_extension in [".json", ".schema"]:
                                continue
                            if not os.path.exists(type_pn):
                                logger.warning("Missing schema file '%s'. Declared in the RAML types section.", type_fn)
                            else:
                                #FIXME: Do we need to weed out "raml-util" etc. paths?
                                schema_files.add(type_pn)
    return sorted(schema_files)

def list_common_schemas(release_api_dir, main_api_dir, schemas_release, schemas_main):
    """Determine the list of schemas that are common between release and main."""
    rel_release = set([])
    rel_main = set([])
    for schema_pn in schemas_release:
        rel_release.add(os.path.relpath(schema_pn, start=release_api_dir))
    for schema_pn in schemas_main:
        rel_main.add(os.path.relpath(schema_pn, start=main_api_dir))
    common = sorted(rel_release.intersection(rel_main))
    old = sorted(rel_release.difference(rel_main))
    new = sorted(rel_main.difference(rel_release))
    return common, old, new

def process_api_schemas(common_schemas, release_api_dir, main_api_dir, output_dir, version):
    """Process the set of common API schemas.
       Store the diff result of each.
       Return the summary of files that were detected as modified.
    """
    files = []
    for schema_fn in common_schemas:
        file_record = {}
        release_pn = os.path.join(release_api_dir, schema_fn)
        main_pn = os.path.join(main_api_dir, schema_fn)
        (status, result) = do_jd(release_pn, main_pn)
        if status:
            if result != "":
                file_record['fileName'] = schema_fn
                file_record['state'] = 'modified'
                files.append(file_record)
                output_fn = os.path.splitext(schema_fn)[0]
                store_diff_result(output_dir, output_fn, result, version, "api")
    return files

def process_api_parent_schemas(common_schemas, release_api_dir, main_api_dir, output_dir, version):
    """Process the set of common dereferenced API parent schemas.
       Store the diff result of each.
       Return the summary of files that were detected as modified.
    """
    files = []
    for schema_fn in common_schemas:
        file_record = {}
        release_pn = os.path.normpath(os.path.join(release_api_dir, "derefparents", schema_fn))
        main_pn = os.path.normpath(os.path.join(main_api_dir, "derefparents", schema_fn))
        if not (os.path.exists(release_pn) and os.path.exists(main_pn)):
            logger.warning("Missing dereferenced input files for '%s'", schema_fn)
            continue
        (status, result) = do_jd(release_pn, main_pn)
        if status:
            if result != "":
                file_record['fileName'] = os.path.join("parents", schema_fn)
                file_record['state'] = 'modified'
                files.append(file_record)
                output_fn = os.path.splitext(schema_fn)[0]
                store_diff_result(output_dir, output_fn, result, version, "apiparents")
    return files

def dereference_schemas(schemas, release_api_dir, main_api_dir):
    """
    Dereference the parent schema files to resolve the $ref child schema.
    """
    script_pn = os.path.join(sys.path[0], "deref-schema.js")
    release_parent_dir = os.path.join(release_api_dir, "derefparents")
    os.makedirs(release_parent_dir, exist_ok=True)
    main_parent_dir = os.path.join(main_api_dir, "derefparents")
    os.makedirs(main_parent_dir, exist_ok=True)
    for schema_fn in schemas:
        release_input_pn = os.path.normpath(os.path.join(release_api_dir, schema_fn))
        release_output_pn = os.path.normpath(os.path.join(release_parent_dir, schema_fn))
        os.makedirs(os.path.split(release_output_pn)[0], exist_ok=True)
        try:
            sh.node(script_pn, release_input_pn, release_output_pn)
        except sh.ErrorReturnCode as err:
            logger.warning("Trouble doing node: %s", err.stderr.decode())
        main_input_pn = os.path.normpath(os.path.join(main_api_dir, schema_fn))
        main_output_pn = os.path.normpath(os.path.join(main_parent_dir, schema_fn))
        os.makedirs(os.path.split(main_output_pn)[0], exist_ok=True)
        try:
            sh.node(script_pn, main_input_pn, main_output_pn)
        except sh.ErrorReturnCode as err:
            logger.warning("Trouble doing node: %s", err.stderr.decode())
        sleep(1)

def store_diff_result(output_dir, output_fn, result, version, store_type):
    """Store the result from jd, and the summary file."""
    (storage_dir_pn, storage_fn) = os.path.split(output_fn)
    if store_type == "api":
        storage_dir = os.path.join(output_dir, "api", storage_dir_pn)
        os.makedirs(storage_dir, exist_ok=True)
        storage_pn = os.path.join(storage_dir, storage_fn)
    elif store_type == "apiparents":
        storage_dir = os.path.join(output_dir, "api", "parents", storage_dir_pn)
        os.makedirs(storage_dir, exist_ok=True)
        storage_pn = os.path.join(storage_dir, storage_fn)
    else:
        storage_dir = output_dir
        storage_pn = os.path.join(storage_dir, output_fn)
    storage_diff_pn = os.path.join(storage_dir, "{}-{}.diff".format(storage_pn, version))
    storage_txt_pn = os.path.join(storage_dir, "{}-{}.txt".format(storage_pn, version))
    with open(storage_diff_pn, "w") as output_fh:
        output_fh.write(result)
        output_fh.write("\n")
    with open(storage_txt_pn, "w") as output_fh:
        output_fh.write("Comparison version: {}\n".format(version))
        output_fh.write("Comparison date: {}\n".format(DATE_TIME))
        output_fh.write("----\n")
        output_fh.write(result)
        output_fh.write("\n")

def show_db_diff(repo_name, mod_name, version, release_sha, branch, db_fn):
    """Show DB schema differences."""
    status = True
    errors = []
    file_record = {}
    output_dir = os.path.join("schemadiff", branch, mod_name)
    os.makedirs(output_dir, exist_ok=True)
    url_base = "https://raw.githubusercontent.com/folio-org/{}".format(repo_name)
    # remove leading "blob/master/"
    url_file = db_fn[12:]
    url_release = os.path.join(url_base, release_sha, url_file)
    url_main = os.path.join(url_base, "master", url_file)
    (status, contents_release) = get_url_contents(url_release)
    if not status:
        errors.append("Could not obtain content for release DB schema")
        return status, errors, file_record
    (status, contents_main) = get_url_contents(url_main)
    if not status:
        errors.append("Could not obtain content for main DB schema")
        return status, errors, file_record
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as fp_1:
        fp_1.write(json.dumps(contents_release, sort_keys=True, indent=2, separators=(",", ": ")))
        fp_1.flush()
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as fp_2:
            fp_2.write(json.dumps(contents_main, sort_keys=True, indent=2, separators=(",", ": ")))
            fp_2.flush()
            (status, result) = do_jd(fp_1.name, fp_2.name)
            if status:
                file_record['fileName'] = url_file
                if result:
                    store_diff_result(os.path.abspath(output_dir), "db", result, version, "db")
                    file_record['state'] = 'modified'
                else:
                    file_record['state'] = 'identical'
            else:
                errors.append("Trouble with jd detecting JSON diff for DB schema")
    return status, errors, file_record

def store_summary(summary_json, branch, mod_name):
    """Store this module's processing summary JSON."""
    output_dir = os.path.join("schemadiff", branch, mod_name)
    os.makedirs(output_dir, exist_ok=True)
    output_fn = os.path.join(output_dir, "summary.json")
    with open(output_fn, "w") as output_fh:
        output_fh.write(json.dumps(summary_json, sort_keys=True, indent=2, separators=(",", ": ")))
        output_fh.write("\n")

def main():
    exit_code = 0
    branch = get_options()
    url_base = "https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/_data"
    url_versions = os.path.join(url_base, "releases-backend-{}.json".format(branch))
    url_repos = os.path.join(url_base, "repos.json")
    json_versions = get_config_data(url_versions)
    # For local testing:
    #with open("_data/releases-backend-{}.json".format(branch), 'r') as json_fh:
        #json_versions = json.load(json_fh)
    json_repos = get_config_data(url_repos)
    global DATE_TIME
    # The yaml parser gags on the "!include".
    # http://stackoverflow.com/questions/13280978/pyyaml-errors-on-in-a-string
    yaml.add_constructor(u"!include", construct_raml_include, Loader=yaml.SafeLoader)
    for mod in json_versions['repos']:
        logger.info("Assessing %s %s", mod['name'], mod['version'])
        # validate_filename prevents path traversal vulnerability.
        # Security scanners like snyk.io notice that json_versions is fetched from a URL
        # and therefore is external (=dangerous) data.
        # CWE-23: https://cwe.mitre.org/data/definitions/23.html
        mod_name = validate_filename(mod['name'])
        repo_name = validate_filename(mod['nameRepo'])
        version = validate_filename(mod['version'])
        DATE_TIME = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
        #test_modules = ['mod-notes', 'mod-configuration']
        #test_modules = ['mod-notes', 'mod-z3950']
        #if not mod_name in test_modules: # testing
            #continue
        summary_json = {}
        summary_json["metadata"] = {}
        summary_json["metadata"]["moduleName"] = mod_name
        summary_json["metadata"]["moduleVersion"] = version
        summary_json["metadata"]["dateProcessed"] = DATE_TIME
        summary_json["processingErrors"] = []
        summary_json["filesModified"] = []
        if not mod['releaseTag']:
            msg = "Missing release Tag"
            logger.warning("%s: %s", mod_name, msg)
            summary_json["processingErrors"].append(msg)
            store_summary(summary_json, branch, mod_name)
            continue
        repo_details = get_repo_details(json_repos, mod_name)
        try:
            has_db_schema = repo_details['hasDbSchema']
        except KeyError:
            pass
        else:
            if has_db_schema: #FIXME: repos.json sometimes has null property
                (status, errors, file_record) = show_db_diff(
                    repo_name, mod_name, version, mod['releaseSha'], branch, has_db_schema)
                if status:
                    logger.debug("%s: has DbSchema", mod_name)
                    summary_json["filesModified"].append(file_record)
                else:
                    summary_json["processingErrors"].extend(errors)
        try:
            ramls_dir = repo_details['ramlDirName']
        except KeyError:
            pass
        else:
            if ramls_dir: #FIXME: repos.json sometimes has null property
                logger.debug("%s: has RAML", mod_name)
                # validate_filepath prevents path traversal vulnerability.
                # Security scanners like snyk.io notice that json_repos is fetched from a URL
                # and therefore is external (=dangerous) data.
                # CWE-23: https://cwe.mitre.org/data/definitions/23.html
                ramls_dir = validate_filepath(ramls_dir)
                (status, errors, files) = show_api_diff(
                    repo_name, mod_name, version, mod['releaseSha'], ramls_dir, branch)
                if status:
                    summary_json["filesModified"].extend(files)
                else:
                    summary_json["processingErrors"].extend(errors)
        store_summary(summary_json, branch, mod_name)
        sleep(3)
    status = prepare_s3_publish(branch)
    logging.shutdown()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
