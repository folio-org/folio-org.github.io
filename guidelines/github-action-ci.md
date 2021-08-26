---
layout: page
title: Configure the GithubAction CI pipeline for UI and Stripes repositories
permalink: /guidelines/github-action-ci/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

These are notes to assist developers with configuring GitHub Actions based CI workflows to replace the currently used Jenkins pipeline.

## Setting up the workflow

### Part I : Configuring For UI and Stripes based repositories

The workflow can be set up by following these steps:
- From the repository navigate to the `Actions`
- On clicking the `New Workflow` button, two NPM based workflows are shown which are developed by FOLIO organization. Make sure to select ONLY those workflows developed by FOLIO. The two NPM based workflows are:
    - **FOLIO NPM Workflow**
    - **FOLIO NPM Release Workflow**
- Once the workflows are added, they need to be configured according to the repository needs.

### Configuring the new Workflow

Each workflow has four environment variables which need to be configured according the requirements of the particular repository. These are:
- **`YARN_TEST_OPTIONS`** -- options to pass to 'yarn test'
- **`SQ_ROOT_DIR`** -- root SQ directory to scan relative to top-level directory
- **`PUBLISH_MOD_DESCRIPTOR`** -- boolean 'true' or 'false'
- **`COMPILE_TRANSLATION_FILES`** -- boolean 'true' or 'false'

For the repositories which have `PUBLISH_MOD_DESCRIPTOR` variable set as true, an extra step needs to be performed.

In the `scripts` attribute of the `package.json` file, the following command needs to be added:
- `"build-mod-descriptor": "stripes mod descriptor --full --strict | jq '.[]' > module-descriptor.json ",`

This triggers the ModuleDescriptor build process.

For repositories where `COMPILE_TRANSLATION_FILES` are set to true, the following changes need to be made to the `package.json` file:
- In the `scripts` attribute, the following command needs to be added:
    - `"formatjs-compile": "formatjs compile-folder --ast --format simple ./translations/ui-users ./translations/users/compiled"`
- Add `"@formatjs/cli": "^4.2.20",` as a devDependency

## Replacing the Jenkins pipeline

The final step is to rename the `Jenkinsfile` into `Jenkinsfile.deprecated` which will stop the Jenkins pipeline to run parallely with the GitHub Action to remove the risk of publishing duplicate artifacts.

## Final Steps

Once the set-up and configuration is done, the workflow can be merged with the default branch and tested.

### Note

Some repositories have the Jenkins CI pipeline set as a required status check for pr_merges. That needs to be removed to configure the Github Workflow successfully.

<div class="folio-spacer-content"></div>

