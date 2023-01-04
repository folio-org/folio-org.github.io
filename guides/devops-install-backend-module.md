---
layout: page
title: DevOps - Install a new back-end module to reference environments
permalink: /guides/devops-install-backend-module/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This document describes procedures for people assisting with [FOLIO DevOps](/guides/devops-introduction/)
to add a new back-end module to the platform-complete and folio-ansible configuration,
and make it available in the folio-snapshot [reference environments](/guides/automation/#reference-environments),
and make it available in the Vagrant box VMs for snapshot.

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

Add to platform-complete snapshot branch.
Make branch in folio-ansible to add to a `group_vars` file.
Make branch in folio-infrastructure to configure Jenkins for a test build.
Configure and test via a special Jenkins job.
Remove testing configuration.
Merge PR to folio-ansible, then to folio-infrastructure.
Follow the daily backend builds to verify.

## Add to snapshot platform

This is the procedure for adding a backend module to the "snapshot" branch of the Stripes Platform [platform-complete](https://github.com/folio-org/platform-complete/tree/snapshot).

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

If approaching the daily [reference environment](/guides/automation/#reference-environments) build times, then the timing of this task can be difficult.

The [build-platform-complete-snapshot](https://jenkins-aws.indexdata.com/job/Automation/job/build-platform-complete-snapshot/) Jenkins build happens every hour, starting at about 19 minutes past and taking about 32 minutes.
This will regenerate the yarn.lock and install files of the Platform, and automatically merge them.

So there will be a short window to prepare the branch and pull-request builds, then merge to "snapshot" branch, then its branch build.

After the next hourly "build-platform-complete-snapshot" run, then verify that the new backend module is now in the [okapi-install.json](https://github.com/folio-org/platform-complete/blob/snapshot/okapi-install.json) file.

If there is trouble, then revert the addition to the Platform, and investigate and report the issues.

## Branch folio-ansible

Make a branch in [folio-ansible](https://github.com/folio-org/folio-ansible),
e.g. `FOLIO-2467-refenvs-ncip`

Add the module to the `group_vars/snapshot` file.
This file assists with building the VMs.
It also currently provides special configuration for some modules
to over-ride LaunchDescriptor settings, or to provide other additional settings.

Follow the format for the entries of other modules.

The "snapshot" file is alphabetically sorted, as Okapi handles the dependency resolution.

The module is declared in the main `folio_modules` section.

If the module is **not** to be pulled in by a front-end UI module via a platform, then it needs to be also declared in the "`add_modules`" section.
Often that is the case because the development of a UI module is not yet ready to require it.
(This `add_modules` section could later be tidied, when that is finally happening.)

## Branch folio-infrastructure

This section explains the preparation for conducting a run of
the [`folio-snapshot-test`](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot-test/) build.

Make a branch in [folio-infrastructure](https://github.com/folio-org-priv/folio-infrastructure),
e.g. `FOLIO-2467-refenvs-ncip`

Add the configuration for the Jenkins job ...

Add to the Jenkinsfile to refer to the folio-infrastructure branch:\
Set Stage:Checkout `branches` variable to be `refs/heads/FOLIO-2467-refenvs-ncip`
(i.e. was `*/master`)

```
CI/jenkins/Jenkinsfile.folio-snapshot-test-build
```

Next refer the git submodule to the folio-ansible branch.
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
[`folio-snapshot-test`](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot-test/) build.

So, select the `Configure` link in the top-left panel.
Then in the section "Pipeline : Pipeline script from SCM : Branches to build" replace "Branch specifier" from `*/master` to `refs/heads/FOLIO-2467-refenvs-ncip` and then "Save".

## Run folio-snapshot-test build

If there have been master changes for folio-ansible and folio-infrastructure since branching, then do merge master to branch, and deal with conflicts.

Before proceeding, visit AWS EC2 - the instance is stopped to save a buck, so temporarily start.

Now run the test build. Select the `Build with Parameters` link in the top-left panel.

Follow the results of this build run via its `Console Output` and full log.

The AWS instance will be removed and rebuilt.
It takes approximately 35-40 minutes.

If not success, then try to interpret the [Jenkins output logfile](/faqs/how-to-investigate-jenkins-logs/).
In some cases, may need to ssh to the instance and inspect the Okapi logfile.

## Verify the test build

After success, then ensure that the new back-end module is in place.
(Example 'curl' of course needs token and tenant headers.)

```
curl -s -S \
  https://folio-snapshot-test-okapi.dev.folio.org/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

Do ssh login to the AWS instance (search the Jenkins build output for "ec2-" to get the DNS name)
and confirm that the module's docker logs are not spewing errors,
and that its docker has not terminated.

Could also verify via the front-end "Settings : Software versions" page (e.g.
[folio-snapshot-test.dev.folio.org](https://folio-snapshot-test.dev.folio.org/settings/about)).

## Finalise

Now that there is happiness, prepare and merge the pull-request to folio-ansible.

Remove the test configuration ...

* At the Jenkins interface for "folio-snapshot-test", revisit its `Configure` page and revert the "Branch specifier" to be `*/master`
(which also signals to other DevOps that you have finished with the test builds).
* Visit AWS EC2 - the "folio-snapshot-test" instance needs to be in "stopped" state to save a buck.

Now make the PR.

Be aware of the timing of the automated back-end build jobs,
as explained at the [reference environments](/guides/automation/#reference-environments).

(If you need to manually run these jobs outside the normal automated schedule, then may need to ask #hosted-reference-envs channel, as people depend on these environments.)

## Inspect build results

Await the scheduled [automated build](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/).

Verify the results of the backend build, as done above.

```
curl -s -S \
  https://folio-snapshot-okapi.dev.folio.org/_/proxy/tenants/diku/modules \
  | jq -r '.[] | select(.id | match("mod-"))[]' | sort
```

Or inspect via the front-end.

## Followup

Delete old branches.

Visit AWS EC2 - the "folio-snapshot-test" instance needs to be in "stopped" state to save a buck.

Comment and close the Jira ticket.

Celebrate.

<div class="folio-spacer-content"></div>

