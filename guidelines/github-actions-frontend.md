---
layout: page
title: Configure GitHub Actions CI pipeline for frontend repositories
permalink: /guidelines/github-actions-frontend/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

These instructions assist developers with configuring GitHub Actions based CI workflows to replace the currently used Jenkins pipeline.

This document is for existing and new front-end UI and Stripes repositories.
For new modules, get the source code and other files in place before adding these workflows.

## Overview

A separate branch and pull request is created for each selected workflow. There are two separate workflows:
1. Snapshot artifacts (FOLIO NPM Workflow)
2. Release artifacts (FOLIO NPM Release Workflow)

## Add FOLIO workflows

The workflows are established by following these steps:
- From the repository GitHub page, navigate to the `Actions` tab.
- On clicking the `New Workflow` button, two NPM based workflows are shown which are developed by FOLIO organization. Make sure to select ONLY those workflows developed by FOLIO. The two NPM based workflows are:
    1. **FOLIO NPM Workflow**
    2. **FOLIO NPM Release Workflow**
- Once the workflows are added, they need to be configured according to the repository requirements.

## Disable Jenkins pipeline

When the first pull request is created with the first workflow, then the Jenkins pipeline needs to be disabled as a first step. This prevents it running in parallel with the GitHub Action workflows and so publishing duplicate artifacts.

Do: `git mv Jenkinsfile Jenkinsfile.deprecated`

After these CI workflows are successfully operating, then that file can be removed.

## Configuration

Each workflow has four environment variables which need to be configured according to the requirements of the particular repository. These are:
- **`YARN_TEST_OPTIONS`** -- options to pass to 'yarn test'
- **`SQ_ROOT_DIR`** -- root SonarQube directory to scan relative to top-level directory
- **`PUBLISH_MOD_DESCRIPTOR`** -- boolean 'true' or 'false'
- **`COMPILE_TRANSLATION_FILES`** -- boolean 'true' or 'false'

For the repositories which have `PUBLISH_MOD_DESCRIPTOR` variable set as true, an extra step needs to be performed:

In the `scripts` attribute of the `package.json` file, the following command needs to be added:
- `"build-mod-descriptor": "stripes mod descriptor --full --strict | jq '.[]' > module-descriptor.json ",`

This triggers the ModuleDescriptor build process.

For repositories where `COMPILE_TRANSLATION_FILES` are set to true, the following changes need to be made to the `package.json` file:
- In the `scripts` attribute, the following command needs to be added:
    - `"formatjs-compile": "formatjs compile-folder --ast --format simple ./translations/ui-users ./translations/users/compiled"`
    - Of course, those "translations" need to follow the [name and layout](/guides/commence-a-module/#front-end-translations) for this particular repository.
- Add `"@formatjs/cli": "^4.2.20",` as a devDependency

## Required status checks

Most repositories have the Jenkins CI pipeline configured as a "Required status check" (`jenkins/pr_merge`). That needs to be removed and the new GitHub CI workflow needs to be added to configure the GitHub Workflow successfully. It can be done in the following way:

- At the tab: "Settings > Branches > Branch protection rules" edit the current rule.
- Remove the Jenkins continuous integration rule.
- Add **`github-actions-ci`** as new required status check.

## Merge to mainline

After the set-up and configuration is done, the workflow can be merged with the default branch and verified.

<div class="folio-spacer-content"></div>
