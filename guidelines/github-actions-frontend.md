---
layout: page
title: Configure GitHub Actions CI pipeline for frontend repositories
permalink: /guidelines/github-actions-frontend/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

These instructions assist developers with configuring GitHub Actions based CI workflows to replace the currently used Jenkins pipeline.

(Note: Either follow this document or wait for the deployment tool that FOLIO DevOps is preparing.)

This document is for existing and new front-end UI and Stripes repositories.
For new modules, get the source code and other files in place before adding these workflows.

## Overview

A separate branch and pull request is created for each selected workflow. There are two separate workflows:
1. Snapshot artifacts (FOLIO NPM Workflow)
2. Release artifacts (FOLIO NPM Release Workflow)

**Note**: Only do this work when your project is not in a busy phase or about to make a release, as one of the steps is to disable the Jenkins pipeline.

**Note**: Someone with Admin rights will need to reconfigure the "CI Checks" before the first workflow PR can be merged.

Do the first workflow branch and PR, and get it merged. Then follow promptly with the second workflow.

## Add FOLIO workflows

The workflows are established by following these steps:
- From the project's repository GitHub page, navigate to the "`Actions`" tab.
- If there is already an existing Workflow, then there will be a "`New Workflow`" button. Selecting it will navigate to the same page: to find and choose a workflow.
- Enter "FOLIO" in the search field. Two NPM based workflows are shown which are developed by FOLIO organization. Make sure to select ONLY those workflows developed by FOLIO. The two NPM based workflows are:
    1. **FOLIO NPM Workflow**
    2. **FOLIO NPM Release Workflow**
- (This procedure ensures using the current version of the FOLIO Workflows. Do not copy from another repository.)
- Select the first workflow.
- Once a workflow is initialised, it needs to be configured according to the repository requirements.

## Configure the Workflow

Each workflow has four environment variables which need to be configured according to the requirements of the particular repository. These quoted variables are:
- **`YARN_TEST_OPTIONS`** -- options to pass to "yarn test"
- **`SQ_ROOT_DIR`** -- root SonarQube directory to scan relative to top-level directory, e.g. `'./src'`
- **`PUBLISH_MOD_DESCRIPTOR`** -- boolean `'true'` or `'false'`
- **`COMPILE_TRANSLATION_FILES`** -- boolean `'true'` or `'false'`

## Start commit

Select the "`Start commit`" button. Provide a branch name.

This will create a new branch and a pull-request.

Now do 'git pull' and checkout this new branch and do the following steps.

## Disable Jenkins pipeline

The Jenkins pipeline needs to be disabled as a first step. This is very important, as it prevents running Jenkins in parallel with the GitHub Action workflows and so publishing duplicate artifacts.

Do: `git mv Jenkinsfile Jenkinsfile.deprecated`

(After these CI workflows are successfully operating, then that file can be removed.)

## Edit package.json

For the repositories which have `PUBLISH_MOD_DESCRIPTOR` variable set as true, an extra step needs to be performed:

In the `scripts` attribute of the `package.json` file, the following command needs to be added:
- `"build-mod-descriptor": "stripes mod descriptor --full --strict | jq '.[]' > module-descriptor.json",`

This triggers the ModuleDescriptor build process.

For repositories where `COMPILE_TRANSLATION_FILES` are set to true, the following changes need to be made to the `package.json` file:
- In the `scripts` attribute, the following command needs to be added:
    - `"formatjs-compile": "formatjs compile-folder --ast --format simple ./translations/ui-users ./translations/ui-users/compiled"`
    - Of course, those "translations" need to follow the [name and layout](/guides/commence-a-module/#front-end-translations) for this particular repository.
- Add `"@formatjs/cli": "^4.2.20",` in the section "devDependencies".

## Push the branch changes

Push the branch.

## Required status checks

Most repositories have the Jenkins CI pipeline configured as a "Required status check" (`jenkins/pr_merge`). That needs to be removed and the new GitHub CI workflow needs to be added to configure the GitHub Workflow successfully. It can be done in the following way:

- At the tab: "Settings > Branches > Branch protection rules" edit the current rule.
- Remove the Jenkins continuous integration rule.
- Add **`github-actions-ci`** as new required status check.

## Merge to mainline

After the set-up and configuration is done, the first workflow can be merged with the default branch and verified.

Then repeat promptly with the second workflow.

## Forked repositories

The workflows cannot be run successfully directly from forked repositories. There are organisation-level secrets required to run CI steps such as "`Run SonarCloud scan`".
The GitHub Actions do not provide access to these secrets, thereby causing the workflow to fail.

To run the workflow and merge the PR, the following steps need to be followed by a committer with write access to the target repository:
- `git remote add $nickname $remote_url`
- `git fetch $nickname`
- `git checkout $branch`
- `git push -u origin head`

The author should tag a **committer** in a comment of the PR to request this assistance, as without commit privileges the author will be unable to directly add reviewers.

<div class="folio-spacer-content"></div>

