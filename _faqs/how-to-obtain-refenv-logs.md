---
layout: page
title: How to obtain reference environment module logs
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 13
---

Developers can obtain the Docker logfiles for backend modules from the [reference environment](/guides/automation/#reference-environments) daily builds.

Visit the self-service facility Jenkins job [collect-reference-env-logs](https://jenkins-aws.indexdata.com/job/Automation/job/collect-reference-env-logs/) (and ensure Jenkins [login](/guides/automation/#jenkins)).

Select "Build with Parameters" from its left-hand panel.

* Define the host from which to fetch, e.g. `folio-snapshot`.
* Declare the list of modules for which to gather their logs.
* Declare the Slack channel or Slack user to notify about the retrieval URL.
For example notify yourself, or another person, or notify your team channel.
* To notify a Slack user, specify the Slack "member ID" which can be found in the Slack user's profile (under "More"). For example `@U999FOOBAR`

All members of folio-org are configured to run this job. The service creates a tar file containing the specified logs (and also the Okapi log) and uploads to an S3 bucket. A URL to retrieve the logs is returned via a Slack notification.

