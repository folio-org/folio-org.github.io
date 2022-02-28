---
layout: page
title: Rename a module
permalink: /guides/rename-module/
menuInclude: no
menuTopTitle: Guides
---

Even though people take care to use an [appropriate name](/guidelines/naming-conventions/#module-names) for a module when it is [commenced](/guidelines/create-new-repo/), it does sometimes become necessary to change the name.

Renaming is often difficult and has various ramifications, so please consider carefully.

## Introduction

Co-ordinate the steps with team members. At an early stage, tell the wider community of the upcoming event.

A general summary follows. The order of steps is loosely proper. Although some will overlap, some may delay others, some may be better done at a different stage.

Some parts can be done by the relevant development teams, while other parts require operations assistance.

## Create tickets

Create Jira [issue tracker](/guidelines/issue-tracker/) tickets to help direct the various parts of the process.
Smaller, well-contained tickets are useful so that each part can be readily completed, and so that various teams and people can be responsible.

## Retain old repository

Do not remove or rename the old git repository, nor remove its release branches.

Its artifacts are still required for past releases, and there may be a need to do bugfix releases.

Also it will still be configured, using the old module name, in [folio-ansible](https://github.com/folio-org/folio-ansible) roles for creating various reference environments, and in platform-complete.

## Archive old repository

Limit the access to the old repository so that no further changes can happen while it is cloned to become the new one.

Modify the GitHub repository "Description" field to prepend the text: `** DEPRECATED: Renamed to xxxx ** `

Deal with any outstanding pull requests.

For front-end modules, ideally perform one more `lokalisepush.py` run to capture any remaining translations under this old repository name.
Otherwise follow-up when [configuring Lokalise](#adjust-lokalise-configuration) for the new repository.

Take note of the Settings for branch protection and teams, which will be applied to the new repository.

Now follow the full procedure [How to archive a GitHub repository](/faqs/how-to-archive-repository/).

## Create spaces at Docker Hub

For back-end modules, [create new spaces](/download/artifacts/#docker-images) at Docker Hub.

## Create repository, do git clone

Create a new, completely empty GitHub repository.

Clone the relevant parts (without release tags) of the old one.
This procedure will also retain the git history.

```
mkdir temp; cd temp
git clone --recursive --single-branch --no-tags \
  https://github.com/folio-org/mod-old
```

Remove Jenkinsfile, so that artifacts are not deployed yet:

```
git mv Jenkinsfile Jenkinsfile-disabled
... and commit
```

Push to master of the new repository:

```
git status
git push https://github.com/folio-org/mod-new
```

## Configure GitHub Settings

The [usual](/guidelines/create-new-repo/) Settings, access for relevant teams, branch protection, required status checks, etc.

The actual status checks can only be enabled after the first pull request.

For guidance, follow the settings of the old one.

## Rename git configuration, source, docs

Replace all mention of the old project name.

Update git project configuration (pom.xml or package.json), descriptors, permissions in ModuleDescriptor, translations, source code, project name in RAML files and JSON schemas, readme, other project description, etc.

For back-end modules: In the ModuleDescriptor, utilise the "[replaces](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json#L17)" feature, e.g.

```
{
 "id" : "new-module-1.2.0"
 "replaces": [ "old-module" ]
},
...
```

## Restore Jenkinsfile

When all old project name strings have been rectified, then restore Jenkinsfile, perhaps still disabling some stages.

```
git mv Jenkinsfile-disabled Jenkinsfile
... and commit
```

Among other things, this gets the initial base Sonar coverage scan.

This will need temporary loosening of the GitHub Settings for branch protection, to push directly to master branch.
Otherwise doing it in a pull request will report failure messages in the Sonar stage, because there is no base scan (subsequent PRs would be okay).

## Adjust Lokalise configuration

Ideally, before Archiving the old repository, perform one more `lokalisepush.py` run to capture any remaining translations under the old name.
If this had not been done, then follow these steps while [configuring Lokalise](/guidelines/create-new-repo/#configure-lokalise) for the new repository.

1. Add the new git repo to Lokalise (as one normally would), substituting these instructions for the pull request configuration.
1. Before adding `en.json` to pull request configuration, add all non-`en.json` files and set to their corresponding languages.
1. Make a pull request in Lokalise to add all non-`en.json` files to Lokalise.
1. Remove all non-`en.json` files from the Lokalise pull request configuration and add `en.json`.  Continue as normal.

## Add to reference environments

After the initial snapshot artifacts have been deployed, add the new module to the snapshot/testing reference environments.

Leave the old one in-place at this stage. It will be [removed](#remove-from-reference-environments) from some environments after other modules in FOLIO CI, that use the old interface name, have upgraded.

## Adjust Stripes Platforms

After initial releases, adjust the configured module name and version in
[platform-core](https://github.com/folio-org/platform-core)
and
[platform-complete](https://github.com/folio-org/platform-complete)
master and snapshot branches.

Follow the [release procedures for platforms](/guidelines/release-procedures/#add-to-platforms).

## Prepare Jira project

Prepare Jira "project". Sometimes best to create new one, and re-key relevant issues. Other times best to rename.

## Adjust website API docs configuration

Configure apidocs if this is an old-configured RAML-related back-end module.

(**Note**: Please migrate to the new CI [configuration](/reference/api/#explain-api-doc). Then we do not need this extra stuff.)

The "lint-raml" and "generate-api-docs" CI jobs will operate properly without configuration, but the web site relies on it.

Follow the apidocs [configuration](/faqs/how-to-configure-api-doc-generation/) documentation.

Add a new entry for the new module to the `_data/api.yml` file. Leave the old one as-is.

In the `_data/apigroup.yml` file, move the old one to the "deprecated" section at the bottom.

## Adjust website source list

Update the list of all [modules](/source-code/map/).

## Remove from reference environments

When other modules in FOLIO CI have updated their use of old interfaces, then the deprecated modules can be removed from hosted/reference environments.

## Verify and notify

Throughout this process there would have already been verification of each step.

Do another visit to the main project resources.

Announce that the new project is ready. Celebrate.

Consider clarifications and other items to enhance this document.
