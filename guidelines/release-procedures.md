---
layout: page
title: Release procedures
permalink: /guidelines/release-procedures/
menuInclude: no
menuTopTitle: Guidelines
---

This document summarises the release procedures for FOLIO projects.

* [Maven-based modules](#maven-based-modules)
* [Stripes and UI modules](https://github.com/folio-org/stripes/blob/master/doc/release-procedure.md)

## Introduction

There are separate notes about the
[FOLIO version-numbering scheme](/guidelines/contributing/#version-numbers)
and the [Build, test, and deployment infrastructure](/guides/automation/).

## Maven-based modules

The procedure is outlined here for "Okapi" and is similar for other back-end Maven-based modules.

### Quick summary {#summary-mvn}

(However follow this complete document for its important information.)

 * `git checkout -b "tmp-release-X.Y.Z"`
 * `vi NEWS.md`
 * `git commit -m "Update NEWS" NEWS.md`
 * `mvn -DautoVersionSubmodules=true release:clean release:prepare`
 * `git push && git push --tags`
 * [Jenkins](https://jenkins-aws.indexdata.com/job/folio-org/): Log in!
 * [GitHub](https://github.com/folio-org): Merge temporary release branch to master. Release notes!
 * [Jira](https://issues.folio.org): Mark as released. Add next versions.
 * [Slack](https://folio-project.slack.com/): Announce on `#general`

`tmp-release-X.Y.Z` is a temporary branch needed because master is usually protected
from straight commits. It should be removed after the release.
If you are working on an unprotected bug fix branch you don't need a temporary branch.

Refer to the following sections for more detail.

### Bug fix releases

Generally we want bug fix releases to occur in separate branches with *only* bug fixes (not to be confused with
temporary release branches). For this purpose, we must create a long-lived release branch. We use the naming scheme
`b` followed by the major and minor versions, for example `b2.17` which will include all bug fixes for version 2.17
(so for 2.17.1 and 2.17.2). In order to avoid lowering down the version in the pom file, you can branch off the
bug fix branch at the point of `[maven-release-plugin] prepare release  .. `
(for example at the point of `2.17.0` but before the pom file specifies `2.18.0-SNAPSHOT`).

### Major / minor releases

Note that `master` represents *both* new features and bug fixes. If there are important new features to be added
while holding back incompatible releases, then a feature branch `b2` could be created, but it is probably not worth the effort
except in very special cases.

### Once: Ensure POM declarations

(You only need to do this once for a project. On subsequent releases you can skip this point.)

For Maven-based projects, the [Maven Release Plugin](//maven.apache.org/maven-release/maven-release-plugin)
is required.  To enable the release plugin, add the following to
the parent POM of the project:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-release-plugin</artifactId>
  <version>2.5.3</version>
  <configuration>
    <preparationGoals>clean verify</preparationGoals>
    <tagNameFormat>v@{project.version}</tagNameFormat>
    <pushChanges>false</pushChanges>
    <localCheckout>true</localCheckout>
  </configuration>
</plugin>
```
FOLIO projects which need to deploy artifacts to the FOLIO Maven repository during the
Maven 'deploy' phase will have the following specified in the project's top-level POM:

```xml
  <distributionManagement>
    <repository>
      <id>folio-nexus</id>
      <name>FOLIO Release Repository</name>
      <url>https://repository.folio.org/repository/maven-releases/</url>
      <uniqueVersion>false</uniqueVersion>
      <layout>default</layout>
    </repository>
    <snapshotRepository>
      <id>folio-nexus</id>
      <name>FOLIO Snapshot Repository</name>
      <uniqueVersion>true</uniqueVersion>
      <url>https://repository.folio.org/repository/maven-snapshots/</url>
      <layout>default</layout>
    </snapshotRepository>
  </distributionManagement>

  <scm>
    <url>https://github.com/folio-org/${artifactId}</url>
    <connection>scm:git:git://github.com/folio-org/${artifactId}.git</connection>
    <developerConnection>scm:git:git@github.com:folio-org/${artifactId}.git</developerConnection>
    <tag>HEAD</tag>
  </scm>
```

Commit all changes to the POM file.

### Ensure that Jira issues are ready

For the issues that are associated with this release, ensure that they reflect reality,
have the relevant `Fix Version` parameter, and are closed.

In Jira you'll generally have at most 3 unreleased versions: Next major, next minor and next bug fix release.
Unreleased versions should be *removed*. It is natural that there will be some versions that are not
released anyway.

### Make a temporary release branch
If you do not have commit access to the master branch (and even if you do), you
can make the release on a branch.
```
git checkout -b "tmp-release-X.Y.Z"
```

### Prepare the news document

Edit `NEWS.md` to add concise descriptions and issue numbers for each major item.
Take extra care with spelling and readability.

```
git commit -m "Update NEWS" NEWS.md
```

Only the release manager should ever need to write to the NEWS file. Using Jira versions and Git log,
they can decide what happened in this branch.

(If everybody writes to NEWS along the way, there will be a conflict for ALL merges.)

### Optional: Update any scripts and descriptors for release version

Update version numbers in places that maven will not do automatically, to be the
version you are about to release. That could be ModuleDescriptors, LaunchDescriptors,
or scripts you use for testing and development.

Often it is not necessary to have any such. You should be using the autogenerated
descriptors from templates. Note that scripts can enable the module without mentioning any
version numbers.

```
git commit -a -m "Towards version X.Y.Z"
```

### Prepare and perform the source release

```
mvn -DautoVersionSubmodules=true release:clean release:prepare
```

(If not yet comfortable, then add the parameter `-DdryRun=true`)

This command will prompt you for input including the release tag/version,
the next post-release SNAPSHOT version, as well as ask you to resolve
any SNAPSHOT dependencies if you have any. Do NOT create releases with
SNAPSHOT dependencies! Selecting the defaults are mostly fine.
Your release tag must be prefixed with 'v' (the default) and you can
always change the next SNAPSHOT version later if necessary.

For the question about the next post-release "new development version", rather than accepting the default which suggests increment of "patch" version, instead specify the next "minor" version.
For example `2.18.0-SNAPSHOT` rather than `2.17.1-SNAPSHOT`

Assuming there are no build errors, then you are ready to push your changes to
GitHub.

```
git push && git push --tags
```

### Optional: Update any scripts and descriptors for next development release

Update version numbers in the same places you did earlier, but now for the
next development version:

```
git commit -a -m "Towards version X.Y.0-SNAPSHOT"
git push
```
(If the push fails, you should have been on a release branch. It is not too late
to switch now! `git checkout -b "release-X.Y.Z"`)

### Build and release artifacts

An 'artifact' in this context could either be a Maven artifact released to the FOLIO
Maven repository, a docker image released to Docker Hub, a Linux distribution package
or some combination of artifacts depending on the project.

After preparing the release as explained above, the next step is done via the [FOLIO Jenkins system](https://jenkins-aws.indexdata.com).
Jenkins credentials utilize the Github authentication for FOLIO core developers, so ensure that you are logged in to GitHub to then enable login to Jenkins.

Select the [Github folio-org](https://jenkins-aws.indexdata.com/job/folio-org/) folder, then follow to the relevant job (e.g.
[mod-circulation](https://jenkins-aws.indexdata.com/job/folio-org/job/mod-circulation/)) and select the "Tags" tab. Select the new release version tag, then the "Build Now" link in the left-hand panel to trigger it.

### Merge the temporary release branch into master
Go to GitHub and make a pull request for the release branch you just pushed.
Wait for all the tests to pass and merge the pull request.

### Add release notes to GitHub

Go to the "Releases" area (e.g.
[Okapi](https://github.com/folio-org/okapi/releases)).
Select `Draft a new release` then choose the tag of the new release and add the NEWS portion
-- *only* the part of NEWS since the previous release.

### Prepare Jira for next release

Use the Jira "Admin" interface of your project to "Manage Versions". Mark the current version as
released, and add the next version(s).

### Announce

Send a note to #general on Slack if relevant.

### Improve this doc

If you found some parts of this guide to be out-of-date, or hard to understand,
now is a good time to fix that. Check out the repository [folio-org/folio-org.github.io](https://github.com/folio-org/folio-org.github.io)
and edit `guidelines/release-procedures.md`

## Stripes-based modules

All Stripes modules (i.e. stripes-* and ui-*) follow the
[Stripes release procedure](https://github.com/folio-org/stripes/blob/master/doc/release-procedure.md).

