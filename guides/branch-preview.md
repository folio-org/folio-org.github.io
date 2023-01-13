---
layout: page
title: Branch preview mode for UI modules
permalink: /guides/branch-preview/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

<div class="attention">
Note: This documentation is outdated.
</div>

Branch preview mode allows developers, product owners, and other interested parties to "preview"
changes to FOLIO UI components on a live FOLIO system before committing them to the master
branch.

**NOTE:** This is a proof-of-concept, applying to selected UI modules: ui-users and ui-requests.

## How it works

A FOLIO backend system is built daily from the master branch of these "platform"
GitHub repositories:
[FOLIO "platform-complete" distribution](https://github.com/folio-org/platform-complete).

These systems contain only the latest releases of Okapi and backend FOLIO modules that are
included in either of the FOLIO platforms listed above.

When a GitHub PR is opened for an existing branch on,  the following "preview" related
processes occur in addition to existing quality gates (unit tests, SonarQube, etc).

* The base set of backend FOLIO modules used in the PR are derived from releases specified in
the master branch of platform-complete (see 'install.json').  However,
there are cases where, in order to adequately test new functionality in a frontend module,
replacing a released module with an unreleased version may be necessary to include in the PR.  
This can be accomplished by specifying the backend module you want to substitute for the
released module in a file called '.pr-custom-deps.json' located in the top-level directory of
your module's repo.  This is a json-formatted file that contains the 'id' of the module you
want to include and the 'action' you want Okapi to take with the module for your tenant -
'enable' or 'disable'.  The following example will deploy and enable snapshot versions of
mod-users-bl and mod-users in place of the default released modules:

    [
      {
        "id" : "mod-users-bl-4.5.0-SNAPSHOT.62",
         "action" : "enable"
      },
      {
        "id" : "mod-users-15.6.0-SNAPSHOT.76",
        "action" : "enable"
      }
    ]

* Code from the UI module's branch is merged into platform-complete.
Essentially replacing the released version of the module.

* A stripes "bundle" or webpack is compiled, and a module descriptor for the module that
is getting previewed is posted to Okapi on the backend FOLIO instance.

* An interface dependency check is conducted via Okapi to ensure that all required interfaces
can be resolved to the existing set of released modules that are deployed on the FOLIO server.

* A tenant is created on the backend FOLIO system for each build iteration of the PR. The tenant
naming convention is "`GITHUB_PROJECT NAME_ + PR_NUMBER_ + JENKINS_BUILD_NUMBER`".
For example, PR 64 for ui-users would create a tenant called 'ui_users_64_1'.  The tenant
admin user for the tenant is the same as the tenant name + 'admin'.  For example, the tenant
admin user for tenant, ui_users_64_1, would be 'ui_users_64_1_admin'.  The tenant admin password
in all cases is 'admin'.

* Tenant modules are enabled, and reference and sample data for select modules are loaded
for the tenant.

* The stripes webpack is distributed to an S3 web service.
The UI is configured for the correct tenant and Okapi instance.
An AWS S3 URL to the UI is appended to the pull request.

All of the above steps happen more or less sequentially, so if a step fails for whatever reason,
the build is marked as 'FAILED'.

## Current limitations

* The UI module must have an interface that is compatible with the existing set of released
modules. If a UI module requires a newer version of an interface from a backend
module, then the backend module must be released first and included in the FOLIO configuration of
released modules contained on the master branch of platform-complete.

* There can be multiple build iterations for each PR.  A new tenant will be created for each
iteration. However, only one Stripes bundle is retained - the one produced from the
latest build iteration.

* The backend FOLIO instance is rebuilt daily.  Therefore, tenants created from the previous
day are no longer accessible and a new tenant must be provisioned by initiating the next
build iteration.  This can be done with either a new commit pushed to the previewed branch or
by initiating a PR build via FOLIO Jenkins.

* When a PR is closed, then all AWS S3 resources associated with the PR are removed.

## Enabling branch preview mode

To enable branch preview mode for a UI module,  the 'stripesPlatform' parameter must
be configured in the repository's Jenkinsfile.

Example configuration:

    buildNPM {
      publishModDescriptor = true
      runLint = false
      runSonarqube = false
      runRegression = true
      runTest = false
      runTestOptions = '--karma.singleRun --karma.browsers ChromeDocker --karma.reporters
                        mocha junit --coverage'
      stripesPlatform = [ repo:'platform-core', branch:'master']
    }

Note: Only 'platform-core' and branch 'master'  is supported at this time.

Additionally, if UI integration tests exist for a UI module,  these tests will also
run during the PR build iteration when 'runRegression' is set to true.

## Feedback

Please post any issues or additional questions to the #devops channel on FOLIO Slack.

