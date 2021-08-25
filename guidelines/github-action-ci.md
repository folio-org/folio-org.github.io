---
layout: page
title: Configure the GithubAction CI pipeline for UI and Stripes repositories
permalink: /guidelines/github-action-ci/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

These are notes to assist developers with configuring Github Action based CI workflows to replace the currently used Jenkins pipeline

## Setting up the workflow

### Part I : Configuring For UI and Stripes based repositories

The workflow can be set up by following these steps
- From the repository navigate to the `Actions`
- On clicking the `New Workflow` button two NPM based workflows can be found developed by FOLIO organization. Make sure the select ONLY the workflows developed by FOLIO. The two NPM based workflows are
    - FOLIO NPM Workflow
    - FOLIO NPM Release Workflow
- Once the workflow is set up it needs to be configured according to the repository needs

### Configuring the new Workflow

The workflow has 4 `environment variables` which need to be configured according the needs of the particular repositories. These are:
- YARN_TEST_OPTIONS (options to pass to 'yarn test')
- SQ_ROOT_DIR (root SQ directory to scan relative to top-level directory)
- PUBLISH_MOD_DESCRIPTOR (boolean 'true' or 'false')
- COMPILE_TRANSLATION_FILES (boolean 'true' or 'false')

They can be configured using the Jenkinsfile.

For the repositories which have `PUBLISH_MOD_DESCRIPTOR` variable set as true, an extra step needs to be performed.

In the `scripts` attribute of the `package.json` the following command needs to be added
- `"build-mod-descriptor": "stripes mod descriptor --full --strict | jq '.[]' > module-descriptor.json ",`

This triggers the module descriptor build process.

For repositories where `COMPILE_TRANSLATION_FILES` are set to true the following changes should be made to the `package.json`
- In the `scripts` attribute the following command needs to be added
    - `"formatjs-compile": "formatjs compile-folder --ast --format simple ./translations/ui-users ./translations/users/compiled"`
- Add `"@formatjs/cli": "^4.2.20",` as a devDependency



## Replacing the Jenkings pipeline

The final step is to rename the `Jenkinsfile` into `Jenkinsfile.deprecated` which will stop the Jenkins pipeline to run parallely with the GitHub Action to remove the risk of publishing duplicate artifacts.

## Final Steps

Once the set-up and configuration is done, the wokflow can be merged with the default branch and tested.

### Note

Some repositories have the Jenkins CI pipeline set as a required status check for pr_merges. That needs to be removed to configure the Github Workflow sucessfully.

<div class="folio-spacer-content"></div>

