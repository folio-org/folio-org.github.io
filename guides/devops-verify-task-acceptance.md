---
layout: page
title: DevOps - Verify task acceptance criteria
permalink: /guides/devops-verify-task-acceptance/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This document describes some common [FOLIO DevOps](/guides/devops-introduction/) related scenarios for the continuous integration and continuous deployment (CI/CD) related infrastructure.
It explains how they are tested and verified for completeness and success, before the changes are "rolled out" into production.

* [Ansible-related features](#ansible-related-features)
* [Jenkins Pipelines shared libraries](#jenkins-pipelines-shared-libraries)

## Ansible-related features

### Introduction {#ansible-introduction}

This scenario involves changes or new Ansible-related features to the
[folio-ansible](https://github.com/folio-org/folio-ansible)
or
[folio-infrastructure](https://github.com/folio-org-priv/folio-infrastructure)
repositories.

These two repos consist of playbooks and roles that automate the provisioning of various FOLIO instances and services.
They are used extensively in our development, test, and CI environments.

Some common DevOps tasks could include adding new modules or wrangling sample data into a FOLIO build environment, adding various options to existing roles to extend functionality, and adding new roles to meet new requirements.

### Preparation {#ansible-preparation}

Work is typically performed in a feature branch of folio-ansible or folio-infrastructure.

The tool "[yq](https://github.com/kislyuk/yq)" is useful for verifying YAML files.

### Testing {#ansible-testing}

The changes are manually tested by running the Ansible playbooks in this branch, either on a local development system or on the `jenkins-aws.indexdata.com` host system.
The latter enables us to test changes that involve use of the AWS infrastructure.

For example, changes that would impact folio-snapshot are tested by performing a build of "folio-snapshot-test" which would build a folio-snapshot system from either a branch of folio-ansible or folio-infrastructure.

If the test build completes successfully, further examination of the instance might be necessary depending on the nature of the changes.

### Deployment {#ansible-deployment}

If everything checks out, the new code is merged to the master branch of the relevant repository.

## Jenkins Pipelines shared libraries

### Introduction {#pipelines-introduction}

This scenario involves changes to Jenkins Pipelines shared libraries.
Jenkins pipelines consist of scripts that automate the build steps and quality gates for individual repo branch and PR builds.

Most of these functions are stored in a Jenkins "shared library" in the repository
[jenkins-pipeline-libs](https://github.com/folio-org/jenkins-pipeline-libs)

### Preparation {#pipelines-preparation}

Work is performed in a feature branch of the jenkins-pipeline-libs repository.

Consider an example: Changes to the pipeline that builds, tests, and deploys Node/NPM modules.
So make a test branch (e.g. `FOLIO-1775-foo-bar`) in jenkins-pipeline-libs and push it.

### Testing {#pipelines-testing}

Select a relevant module repository for testing: in this case NPM-based.
Good candidate modules might be stripes-components or ui-users.

Create branches for each these modules (e.g. `FOLIO-1775-testing-foo-bar`).

Add the following line to the top of each Jenkinsfile, to point to the branch of jenkins-pipeline-libs that is being tested.

```
@Library ('folio_jenkins_shared_libs@FOLIO-1775-foo-bar') _
```

Now push the branches.
When the branch builds in Jenkins, it will test the changes that reside in our `FOLIO-1775-foo-bar` branch of jenkins-pipeline-libs.
Review the output.

If our changes are related to actions taken only during Pull Requests, we could open PRs for our test branches in order to simulate these changes.
Mark the PR title to ensure that people are aware to not merge this.
When finished with testing, the PRs are closed (and not merged).

There are limitations to this approach, however. For example, actions that occur only when building on a repository's master branch, or when performing release builds for modules.
These are often more difficult to test, since testing on a module's master branch might introduce problems into that branch.

### Deployment {#pipelines-deployment}

When satisfied, make a PR in jenkins-pipeline-libs.

After merging, follow some subsequent Jenkins builds to make absolutely sure.

