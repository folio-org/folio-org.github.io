"""AWS Lambda Handler for GitHub web hooks

"""
import os
import string
import json
import pprint
import logging
import urllib2
import boto3
import botocore
import requests

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def set_github_status(repo, sha, state, target_url, description):
    """Send build status to GitHub

    Args:
      repo:
      sha:
      state:
      target_url:
      description:

    Returns:
      none
    """
    LOGGER.info('Entering set_github_status(%s, %s, %s, %s, %s)',
          repo, sha, state, target_url, description)
    data = {
        "state": state,
        "target_url": target_url,
        "description": description,
        "context": "website-build/" + config["overall"]["node-name"]
    }
    r = requests.post("https://api.github.com/repos/" + repo + "/statuses/" + sha,
                      json=data,
                      auth=(config["overall"]["github-username"], github_personal_access_token))
    // Incomplete!


def codebuild_start_build(branch, bucket):
    """Launch a CodeBuild start-build

    Args:
      branch: the branch of the git repo to build
      bucket: the bucket to receive the build artifacts

    Returns:
      No return
    """
    LOGGER.info('Entered codebuild_start_build(%s, %s)', branch, bucket)
    client = boto3.client('codebuild')
    try:
        response = client.start_build(
            projectName='DevDocJekyllBuild',
            sourceVersion=branch,
            environmentVariablesOverride=[
                {
                    'name': 'BUCKET_NAME',
                    'value': bucket,
                    'type': 'PLAINTEXT'
                    },
                ],
            )
        LOGGER.info('Response from codebuild.start_build: %s', pprint.pformat(response))
        if not response or not isinstance(response, dict):
            LOGGER.error('CloudBuild failed: %s', response['Error']['Message'])
            raise RuntimeError("CloudBuild Failed")
        # flag_succeeded = False
        # t_end = time.time() + 60 * 2
        # while time.time() < t_end and not flag_succeeded:
        #     time.sleep(5)
        #     timer = client.batch_get_builds([response['build']['id']])
        #     flag_succeeded = timer['builds'][0]['buildComplete']
        # LOGGER.info(json.dumps(timer))
        # if not flag_succeeded:
        #     LOGGER.error('CloudBuild wait time exceeded. Last status: %s', json.dumps(timer))
        #     raise RuntimeError('CloudBuild wait time exceeded')
    except botocore.exceptions.ClientError as ex:
        LOGGER.error('CloudBuild failed: %s', ex.response['Error']['Message'])
        raise RuntimeError('CloudBuild failed')
    LOGGER.info('Build succeeded')
    return


def normalize_name(name):
    """Normalize a branch name to conform to valid AWS bucket names

    Args:
      Push_branch: the name of the git branch as received from GitHub

    Returns:
      String of the normalized branch name
    """
    LOGGER.info('Entered normalize_name(%s)', name)
    name = name.lower()
    allowed_chars = ''.join([string.ascii_lowercase, string.digits, '-'])
    new_name = ''.join(['-' if c not in allowed_chars else c for c in name])
    max_length = 63 - len('.' + os.environ['DevDocDNSName'])
    new_name = (new_name[:max_length]) if len(new_name) > max_length else new_name
    return new_name


def create_stack(push_branch, branch_name):
    """Create a AWS CloudFormation stack for the branch
    """
    LOGGER.info('Entered create_stack(%s, %s)', push_branch, branch_name)
    template_url = 'https://raw.githubusercontent.com/folio-org/folio-org.github.io/{}/work/amazon-web-services/dev-folio-org-branch_cloudformation.yml'.format(push_branch)  # NOQA pylint: disable=C0301
    try:
        template_req = urllib2.urlopen(template_url)
        stack_template = template_req.read()
    except urllib2.URLError, ex:
        LOGGER.error('URLError = %s', str(ex.reason))
        raise RuntimeError("urllib error to template")
    except Exception:
        import traceback
        LOGGER.error('generic exception: %s', traceback.format_exc())
        raise RuntimeError("generic exception getting to template")

    LOGGER.info('Creating stack for %s', branch_name)
    client = boto3.client('cloudformation')
    stack_name = 'DevDocsBranch-' + branch_name
    try:
        response = client.create_stack(
            StackName=stack_name,
            TemplateBody=stack_template,
            Parameters=[
                {
                    'ParameterKey': 'DevDocBranchLabel',
                    'ParameterValue': branch_name,
                    },
                {
                    'ParameterKey': 'DevDocDNSName',
                    'ParameterValue': os.environ['DevDocDNSName'],
                    }
                ],
            )
        if not response or not isinstance(response, dict) or 'StackId' not in response:
            LOGGER.error('Cloudformation failed: %s', response['Error']['Message'])
            raise RuntimeError("couldn't add branch resources")
        waiter = client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        LOGGER.error('Cloudformation failed: %s', ex.response['Error']['Message'])
        raise RuntimeError('CloudFormation failed')

    stack = client.describe_stacks(StackName=response['StackId'])
    for key in stack['Stacks'][0]['Outputs']:
        if key == 'BucketName':
            stack_bucket = stack[key]
    LOGGER.info('Bucket: %s.  Stack created: %s.', stack_bucket, json.dumps(stack))
    return stack_bucket


def stackexistsfor(branch_name):
    """Test if a CloudFormation stack exists

    Args:
      branch_name: name of branch for which a bucket could exist

    Return:
      True when stack corresponding to branch name exists
    """
    LOGGER.info('Testing to see if stack for branch "%s" exists', branch_name)
    client = boto3.client('cloudformation')
    try:
        client.describe_stacks(StackName='{}.{}'.format(branch_name, os.environ('DevDocDNSName')))
    except botocore.exceptions.ClientError:
        return False
    else:
        return True


def handler(event, context):
    """AWS Lambda handler

    Args:
      event:
      context:

    Returns:
      No return
    """
    print json.dumps(event)
    my_event = event['Records'][0]['Sns']

    gh_event = my_event['MessageAttributes'].get('X-GitHub-Event', '')
    if gh_event != 'push':
        LOGGER.info('Nothing to do with X-GitHub-Event: %s', gh_event)
        return

    try:
        hookdata = json.loads(my_event['Message'])
    except ValueError:
        LOGGER.error("Failed to decode json")
        return {"body": json.dumps({"error": "json decode failure"}), "statusCode": 500}

    required_fields = ['ref', 'created', 'deleted']
    for field in required_fields:
        if field not in hookdata:
            LOGGER.error("No %s in the hook, no processing", field)
            return {
                "body": json.dumps(
                    {"error": "unsupported hook type; missing '{}' information"} % field),
                "statusCode": 400}

    push_branch = hookdata['ref'].replace('refs/heads/', '')
    push_created = hookdata['created']
    push_deleted = hookdata['deleted']

    if push_branch == 'master':
        LOGGER.info("Received push to master branch")
        codebuild_start_build('master', os.environ['DevDocMasterBucket'])
        return

    normalized_branch_name = normalize_name(push_branch)
    if push_deleted == 'true':
        LOGGER.info("Received deleted branch message for %s", push_branch)
        # Do something to delete the branch stack

    if push_created == 'true':
        LOGGER.info("Received created branch message for %s", push_branch)
        try:
            bucket = create_stack(push_branch, normalized_branch_name)
        except RuntimeError, err:
            return {"body": json.dumps({"error": err}), "statusCode": 500}

    if not stackexistsfor(normalized_branch_name):
        LOGGER.warning("Received push for '%s' but stack didn't exist; creating.", push_branch)
        try:
            bucket = create_stack(push_branch, normalized_branch_name)
        except RuntimeError, err:
            return {"body": json.dumps({"error": err}), "statusCode": 500}

    LOGGER.info('Beginning build of %s', push_branch)
    codebuild_start_build(push_branch, bucket)
    return
