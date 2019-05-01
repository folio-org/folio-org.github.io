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

Also it will still be configured, using the old module name, in [folio-ansible](https://github.com/folio-org/folio-ansible) roles for creating various reference environments.

## Archive old repository

Modify the GitHub repository "Description" field to prepend the text: `** DEPRECATED ** `

Deal with any outstanding pull requests.

At GitHub use the "[archive and read-only](https://help.github.com/en/articles/about-archiving-repositories)" Setting.

This will disable push access and pull requests.
It leaves the teams configured, and can be temporarily reversed if needed.
This also enables scripts to avoid "archived" repositories.

Other [deprecation](#deprecate-old-repository) steps can be finished later.

## Create spaces at Docker Hub

For back-end modules, [create new spaces](/download/artifacts/#docker-images) at Docker Hub.

## Create repository, do git clone

Create a new, completely empty GitHub repository.

Clone the relevant parts (without release tags) of the old one:

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
git push https://github.com/folio-org/mod-new
```

## Configure GitHub Settings

The [usual](/guidelines/create-new-repo/) Settings, access for relevant teams, branch protection, required status checks, etc.

The actual status checks can only be enabled after the first pull request.

For guidance, follow the settings of the old one.

## Rename git configuration, source, docs

Replace all mention of the old project name.

Update git project configuration (pom.xml or package.json), descriptors, permissions in ModuleDescriptor, source code, project name in RAML files and JSON schemas, readme, other project description, etc.

In the ModuleDescriptor, utilise the "[replaces](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json)" feature, e.g.

```
{
 "id" : "new-module-1.2.0"
 "replaces": [ "old-module" ]
},
...
```

## Restore Jenkinsfile

When all old project name strings have been rectified, then restore Jenkinsfile, perhaps still disabling some stages.

Among other things, this gets the initial base Sonar coverage scan.

This will need temporary loosening of the GitHub Settings, to push directly to master branch.
Otherwise doing it in a pull request will report failure messages in the Sonar stage, because there is no base scan (subsequent PRs would be okay).

## Adjust Lokalise configuration

See some temporary [notes](https://discuss.folio.org/t/renamed-the-vendor-app-to-organizations-app-and-the-consequences-for-translators/2397)
and [FOLIO-1968](https://issues.folio.org/browse/FOLIO-1968).

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

Configure apidocs if this is a RAML-related back-end module.

The "lint-raml" and "generate-api-docs" CI jobs will operate properly without configuration, but the web site relies on it.

Follow the apidocs [configuration](https://dev.folio.org/reference/api/#configure-api-docs) documentation.

Add a new entry for the new module to the `_data/api.yml` file. Leave the old one as-is.

In the `_data/apigroup.yml` file, move the old one to the "deprecated" section at the bottom.

## Adjust website source list

Edit the list of all [modules](/source-code/).

## Deprecate old repository

Do further deprecation steps, e.g. adjust old README to explain the move.

At GitHub this will require temporarily reversing the "archived" Setting.

```
TODO: Link to new guides/deprecate-repository/ FOLIO-1710
```

## Remove from reference environments

When other modules in FOLIO CI have updated their use of old interfaces, then the deprecated modules can be removed from hosted/reference environments.

## Verify and notify

Throughout this process there would have already been verification of each step.

Do another visit to the main project resources.

Announce that the new project is ready. Celebrate.

Consider clarifications and other items to enhance this document.

