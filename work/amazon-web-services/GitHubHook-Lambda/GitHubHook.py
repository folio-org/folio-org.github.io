"""AWS Lambda Handler for GitHub web hooks

"""
import os
import json
import pprint
import logging
import boto3

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def codebuild_start_build(branch, bucket):
    """Launch a CodeBuild start-build

    Args:
      branch: the branch of the git repo to build
      bucket: the bucket to receive the build artifacts

    Returns:
      No return
    """
    LOGGER.info('Starting CodeBuild with branch "%s" and bucket "%s"', branch, bucket)
    client = boto3.client('codebuild')
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
    return


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

    LOGGER.warning('Maybe shouldn''t have gotten here')
    return
