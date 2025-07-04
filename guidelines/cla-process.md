---
layout: page
title: FOLIO Project Contributor License Agreement
permalink: /guidelines/cla-process/
menuInclude: no
menuTopTitle: Guidelines
---

The FOLIO Project uses the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) for its code and requires developers to acknowledge their contributions to the project using this license.

## Contents of the CLA

The contents of the Contributor License Agreement (CLA) are stored in a Gist on GitHub:

{% gist a72174fc6b18f3a66f2f9d3db1c8f127 %}

The FOLIO Project uses GitHub pull request (PR) required status checks to register a contributor's acknowledgement of the license agreement.
Before a pull request can be merged, all contributors to the pull request must acknowledge their agreement with the terms.
This acknowledgement is through each contributor signing into https://cla-assistant.io/ using their GitHub account.
The screen captures below describe the process.
The acknowledgement of the FOLIO CLA covers all pull requests to the [FOLIO Project GitHub Organization](https://github.com/folio-org).
A new acknowledgement will be required if the text of the CLA changes.

## Enable the CLA required status check

Every project repository at folio-org GitHub organization needs to ensure that the required status check "license/cla" is enabled for pull-requests.
Refer to the required tasks of [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/#branch-protection-and-required-checks).

## Acknowledging the FOLIO Contributor License Agreement

Git repositories in the folio-org GitHub organization have pull request checks that run automated processes when the pull request is made.
One of these checks verifies that all individual committers to the code in the pull request have acknowledged the FOLIO CLA.
When a pull request is made and one of the contributors has not acknowledged the CLA, the CLA-Assistant will add a message to the pull request.

[![Pull request status check without CLA signature](/images/cla-process/1 - Pull request status check without CLA signature.png){:height="50%" width="50%"}](/images/cla-process/1 - Pull request status check without CLA signature.png){:target="_blank"}

Following the "CLA not yet signed" link leads to the CLA-Assistant page with the text of the Contributor License Agreement displayed and a link to sign into the CLA-Assistant via GitHub.

[![Display test of CLA and ask to sign in via GitHub](/images/cla-process/2 - Display text of CLA and ask to sign in via GitHub.png){:height="50%" width="50%"}](/images/cla-process/2 - Display text of CLA and ask to sign in via GitHub.png){:target="_blank"}

GitHub displays a page that asks the contributor to authorize https://cla-assistant.io/ and send that website the contributor's email address.

[![Sign the CLA through GitHub authorization](/images/cla-process/3 - Sign the CLA through GitHub authorization.png){:height="50%" width="50%"}](/images/cla-process/3 - Sign the CLA through GitHub authorization.png){:target="_blank"}

After a few seconds, the contributor is redirected to the GitHub pull request page and the CLA-Assistant pull request check now passes.

[![Pull request status check with CLA signature](/images/cla-process/4 - Pull request status check with CLA signature.png){:height="50%" width="50%"}](/images/cla-process/4 - Pull request status check with CLA signature.png){:target="_blank"}

NOTE: All contributors must acknowledge the CLA before the CLA-Assistant pull request check will pass.

## Fix a stuck status check

Occasionally there is a glitch, whereby this status check fails to register, even though the contributor has already acknowledged their CLA.
The message on the GitHub PR will be something like:\
"license/cla Expected — Waiting for status to be reported".

Being a required status check, this results in hold-ups with the PR.

One cause is when GitHub [status](https://www.githubstatus.com/) is reporting problems with its notifications API, which the CLA agent uses to check PRs.
Another cause might be the busy agent facility.

However, be patient. Sometimes it is just slow, and doing manual refresh might not help.

If it is truly seized, then the status check can be manually refreshed using a URL of the following form.
Replace the `<repo>` with the repository name, and the `<pr-number>` with the pull-request number.

```
https://cla-assistant.io/check/folio-org/<repo>?pullRequest=<pr-number>
```

