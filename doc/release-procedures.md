---
layout: page
title: Release procedures
---

This document summarises the release procedures for FOLIO projects.

<!-- ../../okapi/doc/md2toc -l 2 -h 3 release-procedures.md -->
* [Introduction](#introduction)
* [Maven-based modules](#maven-based-modules)
    * [Ensure POM declarations](#ensure-pom-declarations)
    * [Ensure that JIRA issues are ready](#ensure-that-jira-issues-are-ready)
    * [Prepare the news document](#prepare-the-news-document)
    * [Prepare git and perform the release](#prepare-git-and-perform-the-release)
    * [Add release notes to GitHub](#add-release-notes-to-github)
    * [Prepare JIRA for next release](#prepare-jira-for-next-release)
    * [Announce](#announce)
    * [Other current Maven-related discussion](#other-current-maven-related-discussion)
* [Gradle-based modules](#gradle-based-modules)
  * [Change the release version](#change-the-release-version)
  * [Update to unreleased version](#update-to-unreleased-version)
  * [Trigger the release](#trigger-the-release)
* [Stripes-based modules](#stripes-based-modules)
    * [Other current Stripes-related discussion](#other-current-stripes-related-discussion)

## Introduction

There are separate notes about the general
[build, test, and deployment infrastructure](automation)
and the
[FOLIO version-numbering scheme](http://dev.folio.org/community/contrib-code#version-numbers).

## Maven-based modules

The procedure is outlined here for "Okapi" and is similar for other Maven-based modules.

### Ensure POM declarations

Ensure that the parent POM declares the `maven-release-plugin` and the `distributionManagement`
section as [described](automation).

### Ensure that JIRA issues are ready

For the issues that are associated with this release, ensure that they reflect reality,
have the relevant `Fix Version` parameter, and are closed.

### Prepare the news document

Edit `NEWS.md` to add concise descriptions and issue numbers for each major item.
Take extra care with spelling and readability.

```
git commit -m "Update NEWS" NEWS.md
```

### Prepare git and perform the release

Behind-the-scenes, Jenkins and Maven are assisting.
Review the [automation](automation) steps that will coordinate the release.

Consider for example that we are going to release v1.2.3
so gather these parameters:
* `releaseVersion=1.2.3` -- The version to be released.
* `developmentVersion=1.2.4` -- The next SNAPSHOT version after release version.
If you already know that breaking changes are going to be the next release, then
make that `1.3.0`.

Now initiate the process:

```
mvn -DautoVersionSubmodules=true release:clean release:prepare release:perform \
  -DreleaseVersion=${releaseVersion} -DdevelopmentVersion=${developmentVersion}
```

There will be two commits:
1. Set the POM versions to be 1.2.3 and the git tag is v1.2.3
1. Introduce the SNAPSHOT again.

Watch Jenkins be happy, and [deploy](https://jenkins-aws.indexdata.com/job/okapi-release/) the artifacts.

### Add release notes to GitHub

Go to the "Releases" area (e.g.
[Okapi](https://github.com/folio-org/okapi/releases)).
Select `Draft a new release` then choose the tag of the new release and add the NEWS portion
-- *only* the part of NEWS since previous release.

### Prepare JIRA for next release

Use the "Admin" interface to "Manage Versions". Add the next version.

### Announce

Send a note to Slack if relevant.

### Other current Maven-related discussion

* [OKAPI-287](https://issues.folio.org/browse/OKAPI-287)
  -- Document release procedure
* [OKAPI-265](https://issues.folio.org/browse/OKAPI-265)
  -- Versions in Jira / fix-versions in particular
* [FOLIO-551](https://issues.folio.org/browse/FOLIO-551)
  -- FOLIO release artifacts via Jenkins
* [FOLIO-317](https://issues.folio.org/browse/FOLIO-317)
  -- Identify and implement FOLIO software release process
* [OKAPI-293](https://issues.folio.org/browse/OKAPI-293)
  -- Maven build fails when building from release distributions

## Gradle-based modules

The procedure for [Gradle](https://gradle.org/) based modules (such as [mod-inventory](https://github.com/folio-org/mod-inventory) or [mod-circulation](https://github.com/folio-org/mod-circulation)) is very similar to [maven-based modules](#maven-based-modules).

Follow all of the steps for a maven based module, except [ensure POM declarations](#ensure-pom-declarations) and replacing [performing the release in git](#prepare-git-and-perform-the-release) with the steps outlined below.

### Change the release version

Using the example of releasing version 4.4.0 of the inventory module for context, the top of the [gradle build configuration](https://github.com/folio-org/mod-inventory/blob/master/build.gradle) will look something similar to:

```
apply plugin: 'groovy'
apply plugin: 'application'

mainClassName = "org.folio.inventory.Launcher"
version = "4.3.1-SNAPSHOT"
```

Change the version to "4.4.0" and commit the change using a message similar to "Release v4.4.0".

Create tag representing the release, using a command similar to:

```
git tag -a v4.4.0
```

Describing the changes in this release (similar to those put in the [news](#prepare-the-news-document)) in the annotation of the tag.

### Update to unreleased version

Change the version again to an unreleased snapshot version. In this example it could be "4.4.1-SNAPSHOT" which is the next possible version (or "4.5.0-SNAPSHOT" if the next changes are going to provide new functionality) and commit the change using a message similar to "Increment version number to unreleased version (4.4.1)".

### Trigger the release

Push the changes using commands similar to:

```
git push origin master
git push origin v4.4.0
```

Trigger the appropriate release job in Jenkins to publish the release artefacts, choosing the appropriate tag. In this example the release job is [mod-inventory-release](https://jenkins-aws.indexdata.com/view/Release%20jobs/job/mod-inventory-release/) and the parameter would be the 4.4.0 tag.

## Stripes-based modules

All Stripes modules (i.e. stripes-* and ui-*) follow the
[Stripes release procedure](https://github.com/folio-org/stripes-core/blob/master/doc/release-procedure.md).

### Other current Stripes-related discussion

* [STRIPES-309](https://issues.folio.org/browse/STRIPES-309)
  -- Align git-repos, NPM-packages and Jira projects for Stripes and UI modules.
