---
layout: page
title: DevOps - Install a new back-end module to reference environments
permalink: /guides/devops-install-backend-module/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This document describes procedures for people assisting with [FOLIO DevOps](/guides/devops-introduction/)
to add a new back-end module to the folio-ansible configuration,
and make it available in the folio-snapshot [reference environments](/guides/automation/#reference-environments),
and make it available in the Vagrant box VMs for snapshot and testing.

The developers responsible for that module would have already ensured that the module is ready,
its repository is [established](/guidelines/create-new-repo/),
and is operating in FOLIO CI.
They would have added a Jira ticket, assigned to our team so that we can schedule and track the work.

## Verification and preparation

This is the [relevant guide](/guides/install-backend-module/) that they would have followed.
Still, we need to follow it again.
There are tips not repeated here, and it defines verification steps that would be wise to re-follow before committing to infrastructure configuration.

If they have not indicated on their Jira ticket that they have verified that the module will install on a local VM, then remind them to follow the [Ensure recent local VM](/guides/install-backend-module/#ensure-recent-local-vm) instructions.
Otherwise it could be a huge waste of your time.

Investigate the module README and LaunchDescriptor in case there are other special requirements.

## Overview

Make branch in folio-ansible to add to `group_vars` files.
Make branch in folio-infrastructure to add to a special file, and also to configure Jenkins.
Configure and test via special Jenkins jobs.
Remove testing configuration.
Merge PR to folio-ansible, then to folio-infrastructure.
Follow the daily backend builds to verify.

## Branch folio-ansible

Make a branch in [folio-ansible](https://github.com/folio-org/folio-ansible),
e.g. `FOLIO-2467-refenvs-ncip`

Add the module to the `group_vars/testing` and `group_vars/snapshot` files.
These files also assist with building the VMs, and currently provide special configuration for some modules.

Always add new modules to `group_vars/testing`.

Only add module entries to `group_vars/snapshot` if they need special configuration to over-ride LaunchDescriptor settings, or to provide other additional settings.

If this is also a "core" module, then it will also be added to the corresponding `-core` files.
Normally only added to the main "complete" environments.

Follow the format for the entries of other modules.

Note that the "snapshot" files are alphabetically sorted, as Okapi handles those.

However, the "testing" files have explicit order.
The sequence must have the new module declared after the modules that provide its interfaces (see [verification](#verification-and-preparation) step above).

Also note that for the "snapshot" files, the module is declared in the main section.
If the module is not to be pulled in by a front-end UI module via a platform, then it needs to be also declared in the "`add_modules`" section.
Often that is the case because the development of a UI module is not yet ready to require it.
(This `group_vars` section could later be tidied, when that is finally happening.)

## Branch folio-infrastructure

Make a branch in [folio-infrastructure](https://github.com/folio-org-priv/folio-infrastructure),
e.g. `FOLIO-2467-refenvs-ncip`

Add to `CI/ansible/testing-add-modules.yml` file.
The purpose of this file is to declare modules (e.g. mod-ldp) that are not added to a VM (see the previous [section](#branch-folio-ansible)) but do need to be added to the folio-testing reference environment.

Add the entry to both sections: Register and Deploy.
Follow the format for the entries of other modules.
The sequence must have the new module declared after any modules that provide its interfaces (see [verification](#verification-and-preparation) step above).

Add testing configuration for the Jenkins jobs ...

Add to the Jenkinsfiles to refer to the folio-infrastructure branch:\
Set `BRANCH_TO_BUILD` variable to be `refs/heads/FOLIO-2467-refenvs-ncip`

```
CI/jenkins/Jenkinsfile.folio-testing-test-build
CI/jenkins/Jenkinsfile.folio-snapshot-test-build
```

Refer the git submodule to the folio-ansible branch.
Take care, as this is a tab-delimited file.

Edit the `.gitmodules` file:

```
[submodule "CI/ansible/folio-ansible"]
        path = CI/ansible/folio-ansible
        url = https://github.com/folio-org/folio-ansible
        branch = FOLIO-2467-refenvs-ncip  # <<< add this line <<<
```

Push the folio-ansible branch and the folio-infrastructure branch.

## Jenkins testing configuration

Do [login](/guides/automation/#jenkins) to Jenkins, and modify the configuration for the
[`folio-testing-test`](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-testing-test/) build.
That is the most important test build, due to the explicit order of modules.

So, select the `Configure` link in the top-left panel.
Then in the section "Pipeline : Pipeline script from SCM : Branches to build" replace "Branch specifier" from `*/master` to `refs/heads/FOLIO-2467-refenvs-ncip` and then "Save".

## Run folio-testing-test build

If there have been master changes for folio-ansible and folio-infrastructure since branching, then do merge master to branch, and deal with conflicts.

Now run the test build. Select the `Build with Parameters` link in the top-left panel.

Follow the results of this build run via its `Console Output` and full log.

The AWS instance will be removed and rebuilt.
It takes approximately 20-25 minutes.

If not success, then try to interpret the [Jenkins output logfile](/faqs/how-to-investigate-jenkins-logs/).
In some cases, may need to ssh to the instance and inspect the Okapi logfile.

## Verify the testing build

After success, then ensure that the new back-end module is in place.
(Example 'curl' of course needs token and tenant headers.)

```
curl -s -S \
  https://folio-testing-test-okapi.dev.folio.org/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

Do ssh login to the AWS instance (search the Jenkins build output for "ec2-" to get the DNS name)
and confirm that the module's docker logs are not spewing errors.

Could also verify via the front-end "Settings : Software versions" page (e.g.
[folio-testing-test.dev.folio.org](https://folio-testing-test.dev.folio.org/settings/about)).
However remember that an automated job might be in-process to rebuild its front-end,
as explained at the [reference environments](/guides/automation/#reference-environments).

## Add to snapshot platform

This is the separate procedure for adding a backend module to the "snapshot" branch of the Stripes Platform (e.g. to [platform-complete](https://github.com/folio-org/platform-complete/tree/snapshot)).

Before doing this, the successful build of "folio-testing-test" (described in the preceding sections) will provide some comfort, but it is not a thorough test.
Of course, it it fails then there is no point doing this section.

### Platform explanation

The normal process is that a UI module will require interfaces that are provided by back-end modules (declared in the "okapiInterfaces" section of their package.json file).
With this, the relevant back-end modules are automatically included.
(See separate procedure to [install a new front-end module](/guides/install-frontend-module/).)

However often the front-end and back-end are not yet ready for each other.

If so, then temporarily add the new back-end module to the `install-extras.json` file of the "snapshot" branch of the relevant platform.
(Note that "core" modules are added to both platform-core and platform-complete.)

After the back-end development is eventually ready, then a front-end module will require this module.
When that happens, then the backend module will be automatically included via the normal process, so it can then be removed from this `install-extras.json` file.

However some back-end modules are never required by front-end modules.
In these cases they are always configured in that file.

### Platform configuration

If approaching the daily [reference environment](https://dev.folio.org/guides/automation/#reference-environments) build times, then the timing of this task can be difficult.

The [build-platform-complete-snapshot](https://jenkins-aws.indexdata.com/job/Automation/job/build-platform-complete-snapshot/) Jenkins build happens every hour, starting at about 20 minutes past and taking 30 minutes.
This will regenerate the yarn.lock and install files of the Platform, and automatically merge them.

So there will be a short window to prepare the branch and pull-request builds, then merge to "snapshot" branch, then its branch build.

After the next "build-platform-complete-snapshot" run, then verify that the new backend module is now in the [okapi-install.json](https://github.com/folio-org/platform-complete/blob/snapshot/okapi-install.json) file.

### Run folio-snapshot-test build

Run and verify the [`folio-snapshot-test`](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot-test/) build, as [explained above](#run-folio-testing-test-build) for the "folio-testing-test" build.

If there is trouble, then revert the addition to the Platform, and investigate and report the issues.

## Do pull requests

Now that there is happiness, prepare and merge the pull-requests to folio-ansible and folio-infrastructure.

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

Now await the scheduled [automated builds](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/).

Verify the results of each backend build, as done above.

```
curl -s -S \
  https://folio-testing-okapi.dev.folio.org/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

To inspect via the front-end, note that the folio-testing-stripes build will automatically follow folio-testing-backend for example.

## Followup

Delete old branches.

Comment and close the Jira ticket.

Celebrate.

<div class="folio-spacer-content"></div>

