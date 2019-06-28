# Hosting a Jekyll-based website on AWS, with branch support

(Note: This is outdated. See [FOLIO-1692](https://issues.folio.org/browse/FOLIO-1692).)

## AWS CloudFormation Configuration Files
* [website-master](website-master_cloudformation.yml): Stack of the fundamental components for hosting the website, including the GitHub hook user, the CloudFront distribution, and the S3 bucket hosting the master branch of the site.
* [website-branch](website-branch_cloudformation.yml): Stack of the AWS components needed to host a branch of the website.

## Parameters
Each of these are parameters to the `website-master_cloudformation.yml` file.
In each numbered line, the CloudFormation variable name is listed at the beginning.
1. `WebsiteCFNArtifactsBucket`: S3 bucket for holding artifacts required for the CloudFormation stack (e.g. the AWS Lambda code)
2. `WebsiteDNSName`: DNS name where the website will be located
3. `GitHubWebsiteRepoURL`: URL to the git repository located on GitHub.com
4. `GitHubHookUserName`: Name of the AWS IAM user that will be used on GitHub as the recipient of GitHub Webhook messages

## Stack Creation Process
1. Create a private S3 bucket to contain to contain the AWS Lambda code and other artifacts of the website build process.  Name the bucket something like `dev-website-cloudformation-artifacts`; the name of this bucket is the `WebsiteCFNArtifactsBucket` parameter
1. Create a ZIP file of the Lambda code: `cd GitHubHook-Lambda && zip -g GitHubHook-Lambda.zip GitHubHook.py && cd -`
1. Upload the Lambda code to the private S3 bucket.  For instance, this AWS CLI command: `aws --profile <profile_name> s3 cp GitHubHook-Lambda/GitHubHook-Lambda.zip s3://dev-website-cloudformation-artifacts`
1. Upload `website-branch_cloudformation.yml` to the same bucket: `aws --profile <profile_name> s3 cp website-branch_cloudformation.yml s3://dev-website-cloudformation-artifacts`


## URLs with information that was helpful in creating this CloudFront Stack
* [Dynamic GitHub Actions with AWS Lambda | AWS Compute Blog](https://aws.amazon.com/blogs/compute/dynamic-github-actions-with-aws-lambda/)
* [Using AWS CodePipeline and CodeBuild to update a Jekyll website](https://alexbilbie.com/2016/12/codebuild-codepipeline-update-jekyll-website/)
* [Automated static website deployments via AWS and GitHub](https://www.dadoune.com/blog/aws-codepipeline-cloudbuild-static-s3-website/)
* [Triggering a Lambda from SNS using CloudFormation](https://iangilham.com/2016/03/22/Sns-trigger-lambda-via-cloudformation.html)
* [Subscribing AWS Lambda Function to SNS Topic with CloudFormation](https://e5k.de/subscribing-aws-lambda-function-to-sns-topic-with-cloudformation/)
* [Monitor your AWS CodeBuilds via Lambda and Slack – Hacker Noon](https://hackernoon.com/monitor-your-aws-codebuilds-via-lambda-and-slack-ae2c621f68f1)
