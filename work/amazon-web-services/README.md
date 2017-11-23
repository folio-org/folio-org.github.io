# How dev.folio.org is hosted on AWS

## AWS CloudFormation Configuration Files
* [dev-folio-org-master](dev-folio-org-master_cloudformation.yml): Stack of the fundamental components for hosting dev.folio.org, including the GitHub hook user, the CloudFront distribution, and the S3 bucket hosting the master branch of the docs.

## URLs with helpful information
* [Using AWS CodePipeline and CodeBuild to update a Jekyll website](https://alexbilbie.com/2016/12/codebuild-codepipeline-update-jekyll-website/)
* [Automated static website deployments via AWS and GitHub](https://www.dadoune.com/blog/aws-codepipeline-cloudbuild-static-s3-website/)
* [Triggering a Lambda from SNS using CloudFormation](https://iangilham.com/2016/03/22/Sns-trigger-lambda-via-cloudformation.html)
* [Subscribing AWS Lambda Function to SNS Topic with CloudFormation](https://e5k.de/subscribing-aws-lambda-function-to-sns-topic-with-cloudformation/)
