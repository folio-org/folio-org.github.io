---
layout: page
title: DevOps - Install a new back-end module to reference environments
permalink: /guides/devops-install-backend-module/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This document describes procedures for people assisting with [FOLIO DevOps](/guides/devops-introduction/)
to add a new back-end module to the folio-ansible configuration, and make it available in the folio-snapshot and folio-testing [reference environments](/guides/automation/#reference-environments).

The developers responsible for that module would have already ensured that the module is ready,
its repository is [established](/guidelines/create-new-repo/),
and is operating in FOLIO CI.
They would have added a Jira ticket, assigned to our team so that we can schedule and track the work.

## Verification and preparation

This is the [relevant guide](/guides/install-backend-module/) that they would have followed.
Still, we need to follow it again.
There are tips not repeated here, and it defines verification steps that would be wise to re-follow before committing to infrastructure configuration.

Investigate the module README in case there are other special requirements.

## Overview

Make branch in folio-ansible to add to `group_vars` files.
Make branch in folio-infrastructure to add to a special file, and also to configure Jenkins.
Configure and test via special Jenkins jobs.
Remove testing configuration.
Merge PR to folio-ansible, then to folio-infrastructure.
Follow the daily backend builds to verify.

## Branch folio-ansible

Make a branch in [folio-ansible](https://github.com/folio-org/folio-ansible),
e.g. `folio-2467-refenvs-ncip`

Add the module to the `group_vars/snapshot` and `group_vars/testing` files.

If this is also a "core" module, then it will also be added to the corresponding `-core` files.

Follow the format for the entries of other modules.

Note that the "snapshot" files are alphabetically sorted, as Okapi handles those.

However, the "testing" files have explicit order.
The sequence must have the new module declared after the modules that provide its interfaces (see [verification](#verification-and-preparation) step above).

Also note that for the "snapshot" files, the module is declared in the main section.
If the module is not to be pulled in by a front-end UI module, then it needs to be also declared in the "`add_modules`" section.
Often that is the case because the development of a UI module is not yet ready to require it.
(This section could later be tidied, when that is finally happening.)

Push the branch.

## Branch folio-infrastructure

Make a branch in [folio-infrastructure](https://github.com/folio-org-priv/folio-infrastructure),
e.g. `folio-2467-refenvs-ncip`

Add to `CI/ansible/testing-add-modules.yml` for both sections: Register and Deploy.
Follow the format for the entries of other modules.

The sequence must have the new module declared after any modules that provide its interfaces (see [verification](#verification-and-preparation) step above).

Add testing configuration for the Jenkins jobs ...

Add to the Jenkinsfiles to refer to the folio-infrastructure branch:
Replace `*/master` with `refs/heads/folio-2467-refenvs-ncip`

```
CI/jenkins/Jenkinsfile.folio-testing-test-build
CI/jenkins/Jenkinsfile.folio-snapshot-test-build
```

Add git submodule to refer to the folio-ansible branch.
Take care, as this is a tab-delimited file.

Edit the `.gitmodules` file:

```
[submodule "CI/ansible/folio-ansible"]
        path = CI/ansible/folio-ansible
        url = https://github.com/folio-org/folio-ansible
        branch = folio-2467-refenvs-ncip  # <<< add this line <<<
```

Push the branch.

## Jenkins testing configuration

Do [login](/guides/automation/#jenkins) to Jenkins, and modify the configuration for the
[`folio-testing-test`](https://jenkins-aws.indexdata.com/job/Automation/job/folio-testing-test/) build.
That is the most important test build, due to the explicit order of modules.

The [`folio-snapshot-test`](https://jenkins-aws.indexdata.com/job/Automation/job/folio-snapshot-test/)
build could also be used, but here only explaining one of them.

So, select the `Configure` link in the top-left panel.
Then in the section "Pipeline : Pipeline script from SCM : Branches to build" replace "Branch specifier" from `*/master` to `refs/heads/folio-2467-refenvs-ncip` and then "Save".

## Run the testing build

If there have been master changes for folio-ansible and folio-infrastructure since branching, then do merge master to branch, and deal with conflicts.

Now run the test build. Select the `Build with Parameters` link in the top-left panel.

Follow the results of this build run via its `Console Output` and full log.

The AWS instance will be removed and rebuilt.
It takes approximately 20-25 minutes.

If not success, then try to interpret the log.
Some "Find in page" searches are a bit helpful
(e.g. "failed:" and "fatal:" and "Missing dependency:").

## Verify the testing build

After success, then ensure that the new back-end module is in place:

```
curl -s -S \
  https://folio-testing-test-okapi.aws.indexdata.com/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

Could also do ssh login to the AWS instance (search the output for "ec2-" to get the DNS name)
and verify the module's docker logs.

Could also verify via the front-end "Settings : Software versions" page (e.g.
[folio-testing-test.aws.indexdata.com](https://folio-testing-test.aws.indexdata.com/settings/about)
or
[folio-snapshot-test.aws.indexdata.com](https://folio-snapshot-test.aws.indexdata.com/settings/about)).
However remember that an automated job might be in-process to rebuild its front-end
(as explained at the [reference environments](/guides/automation/#reference-environments).

## Do pull requests

Now that there is happiness, prepare and merge the pull-requests.

First be sure to remove all test configuration ...

* At the Jenkins interface for "folio-testing-test" and "folio-snapshot-test", revisit its `Configure` page and revert the "Branch specifier" to be `*/master`
(which also signals to other DevOps that you have finished with the test builds).
* In the "folio-infrastructure" branch, remove the testing configuration in the Jenkinsfiles
and the gitmodules file.

Now make the PRs.

Be aware of the timing of the automated back-end build jobs,
as explained at the [reference environments](/guides/automation/#reference-environments).

(If you need to manually run these jobs outside the normal automated schedule, then may need to ask #hosted-reference-envs channel, as people depend on these environments.)

First merge to folio-ansible, then to folio-infrastructure.

## Inspect build results

Following the merges, might want to re-run the folio-testing-test build using this now-deployed configuration to ensure no glitches.

Now await the scheduled [automated builds](https://jenkins-aws.indexdata.com/job/Automation/).

Verify the results of each backend build, as done above.
Remember that folio-snapshot-load will be the same as folio-snapshot.

```
curl -s -S \
  https://folio-testing-okapi.aws.indexdata.com/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

To inspect via the front-end, note that the folio-testing-stripes build will automatically follow folio-testing-backend for example.

## Followup

Delete old branches.

Comment and close the Jira ticket.

Celebrate.

