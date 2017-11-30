"""AWS Lambda Handler for GitHub web hooks

"""
import os
import string
import base64
import json
import pprint
import logging
import urllib2
import boto3
import botocore

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

CONST_BUCKET_NAME = 'BUCKET_NAME'
CONST_GITHUB_STATUSES_URL = 'GITHUB_STATUSES_URL'


def set_github_status(statuses_url, state, target_url, description):
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
    LOGGER.info('Entering set_github_status(%s, %s, %s, %s)',
                statuses_url, state, target_url, description)
    data = {
        "state": state,
        "target_url": target_url,
        "description": description,
        "context": "continuous-integration/website-build",
        }
    encoded_data = json.dumps(data)
    LOGGER.info(encoded_data)
    request = urllib2.Request(statuses_url, encoded_data)
    request.add_header("Content-Type", 'application/json')
    auth = base64.encodestring('%s:%s' % (os.environ['GitHubUsername'], os.environ['GitHubAccessToken'])).replace('\n', '')  # NOQA pylint: disable=C0301
    request.add_header("Authorization", "Basic %s" % auth)

    urllibhandler = urllib2.HTTPSHandler(debuglevel=0)
    opener = urllib2.build_opener(urllibhandler)
    urllib2.install_opener(opener)
    try:
        connection = urllib2.urlopen(request)
    except urllib2.HTTPError as ex:
        LOGGER.exception(ex)
        raise RuntimeError('GitHub Status API Update failed: %s', ex.message)

    LOGGER.info('Received status code "%s" from GitHub', connection.code)
    if connection.code != 201:
        raise RuntimeError('Post to GitHub Status API returned "%s", not 201', connection.code)
    LOGGER.info('Leaving set_github_status()')
    return


def codebuild_start_build(branch, bucket, statuses_url):
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
            projectName=os.environ['WebsiteStackName'] + '-WebsiteJekyllBuild',
            sourceVersion=branch,
            environmentVariablesOverride=[
                {
                    'name': CONST_BUCKET_NAME,
                    'value': bucket,
                    'type': 'PLAINTEXT'
                    },
                {
                    'name': CONST_GITHUB_STATUSES_URL,
                    'value': statuses_url,
                    'type': 'PLAINTEXT'
                    },
                ],
            )
        LOGGER.info('Response from codebuild.start_build: %s', pprint.pformat(response))
        if not response or not isinstance(response, dict):
            LOGGER.error('CloudBuild failed: %s', response['Error']['Message'])
            raise RuntimeError("CloudBuild Failed")
    except botocore.exceptions.ClientError as ex:
        LOGGER.error('CloudBuild failed: %s', ex.response['Error']['Message'])
        raise RuntimeError('CloudBuild failed')
    LOGGER.info('Build started')
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
    max_length = 63 - len('.' + os.environ['WebsiteDNSName'])
    new_name = (new_name[:max_length]) if len(new_name) > max_length else new_name
    return new_name


def get_stack_dns(branch_name):
    """Create stack name string
    """
    return '.'.join([branch_name, os.environ['WebsiteDNSName']])


def get_stack_name(branch_name):
    """Create stack name string
    """
    return os.environ['WebsiteStackName'] + 'Branch-' + branch_name


def create_stack(push_branch, branch_name):
    """Create a AWS CloudFormation stack for the branch
    """
    LOGGER.info('Entered create_stack(%s, %s)', push_branch, branch_name)
    template_url = 'https://s3.amazonaws.com/{}/website-branch_cloudformation.yml'.format(os.environ['WebsiteCFNArtifactsBucket'])  # NOQA pylint: disable=C0301

    LOGGER.info('Creating stack for %s', branch_name)
    client = boto3.client('cloudformation')
    stack_name = get_stack_name(branch_name)
    try:
        response = client.create_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            NotificationARNs=[os.environ['WebsiteBranchCFNNotification']],
            Parameters=[
                {
                    'ParameterKey': 'WebsiteBranchLabel',
                    'ParameterValue': branch_name,
                    },
                {
                    'ParameterKey': 'WebsiteDNSName',
                    'ParameterValue': os.environ['WebsiteDNSName'],
                    }
                ],
            )
        if not response or not isinstance(response, dict) or 'StackId' not in response:
            LOGGER.error('Cloudformation failed: %s', response['Error']['Message'])
            raise RuntimeError("couldn't add branch resources")
        waiter = client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        LOGGER.exception(ex)
        raise RuntimeError('CloudFormation failed')
    LOGGER.info('Leaving create_stack()')
    return


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
        client.describe_stacks(StackName=get_stack_name(branch_name))
    except botocore.exceptions.ClientError:
        LOGGER.info('Not found')
        return False
    else:
        LOGGER.info('Found!')
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

    gh_event = my_event['MessageAttributes'].get('X-Github-Event', '')
    if gh_event['Value'] != 'push':
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
    statuses_url = hookdata['repository']['statuses_url']
    sha = hookdata['after']
    statuses_url = statuses_url.replace('{sha}', sha)
    LOGGER.info("Ref: %s; Created: %s; Deleted: %s; statuses_url: %s",
                push_branch, push_created, push_deleted, statuses_url)

    if push_branch == 'master':
        LOGGER.info("Received push to master branch")
        codebuild_start_build('master', os.environ['WebsiteMasterBucket'], statuses_url)
        return

    normalized_branch_name = normalize_name(push_branch)
    if push_deleted:
        LOGGER.info("Received deleted branch message for %s", push_branch)
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(get_stack_dns(normalized_branch_name))
        for obj in bucket.objects.filter():
            s3.Object(bucket.name, obj.key).delete()
        LOGGER.info("S3 bucket contents deleted")

        cloudformation = boto3.resource('cloudformation')
        stack = cloudformation.Stack(get_stack_name(normalized_branch_name))
        try:
            stack.delete()
        except RuntimeError as ex:
            LOGGER.exception(ex)
            return {"body": json.dumps({"error": str(ex)}), "statusCode": 500}
        LOGGER.info("Request to delete stack accepted")
        return

    try:
        set_github_status(statuses_url, 'pending', '', 'Branch build started')
    except RuntimeError as ex:
        return {"body": json.dumps({"error": str(ex)}), "statusCode": 500}

    if push_created:
        LOGGER.info("Received created branch message for %s", push_branch)
        try:
            create_stack(push_branch, normalized_branch_name)
        except RuntimeError as ex:
            return {"body": json.dumps({"error": str(ex)}), "statusCode": 500}

    if not stackexistsfor(normalized_branch_name):
        LOGGER.warning("Received push for '%s' but stack didn't exist; creating.", push_branch)
        try:
            create_stack(push_branch, normalized_branch_name)
        except RuntimeError as ex:
            return {"body": json.dumps({"error": str(ex)}), "statusCode": 500}

    LOGGER.info('Beginning build of %s', push_branch)
    codebuild_start_build(push_branch, get_stack_dns(normalized_branch_name), statuses_url)
    return


def branch_cfn_handler(event, context):
    """AWS Lambda handler for events from the branch CloudFormation stack build

    Args:
      event:
      context:

    Returns:
      No return
    """
    print json.dumps(event)
    LOGGER.info('Beginning build of %s', push_branch)
    codebuild_start_build(push_branch, bucket)
    return


def codebuilder_result_handler(event, context):
    """AWS Lambda handler for events from the CodeBuild project

    Args:
      event:
      context:

    Returns:
      No return
    """
    LOGGER.info('Entering codebuilder_result_handler()')
    print json.dumps(event)
    try:
        build_status = event['detail']['build-status']
        build_env_vars = event['detail']['additional-information']['environment']['environment-variables']
        for build_env_var in build_env_vars:
            if build_env_var['name'] == CONST_BUCKET_NAME:
                bucket_name = build_env_var['value']
            if build_env_var['name'] == CONST_GITHUB_STATUSES_URL:
                statuses_url = build_env_var['value']
    except KeyError as ex:
        LOGGER.exception(ex)
        raise Exception('Unexpected data from CodeBuild Event')
    reported_status = 'success' if build_status == 'SUCCEEDED' else 'failure'
    target_url = 'http://{}.s3-website-{}.amazonaws.com'.format(
        bucket_name, os.environ['AWS_DEFAULT_REGION'])
    set_github_status(statuses_url, reported_status, target_url, 'Branch build finished')
    return
