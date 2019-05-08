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
* [Add to platforms](#add-to-platforms)

## Introduction

There are separate notes about the
[FOLIO version-numbering scheme](/guidelines/contributing/#version-numbers)
and the [Build, test, and deployment infrastructure](/guides/automation/).

## Maven-based modules

The procedure is outlined here for "Okapi" and is similar for other back-end Maven-based modules.

### Quick summary major/feature release {#summary-mvn}

(However follow this complete document for its important information.)

In this example we are releasing `X.Y.0` of a module.

```
 git checkout -b tmp-release-X.Y.0
 vi NEWS.md
 git commit -m "Update NEWS" NEWS.md
 mvn -DautoVersionSubmodules=true release:clean release:prepare # Supply next feature (X.Y+1.0-SNAPSHOT)
 git push && git push --tags
```
Log in to Jenkins and run your jobs at [Jenkins](https://jenkins-aws.indexdata.com/job/folio-org/).

[GitHub](https://github.com/folio-org): Merge temporary release branch `tmp-release-X.Y.0` to master.

[Jira](https://issues.folio.org): Mark as released. Add next versions.

[Slack](https://folio-project.slack.com/): Announce on `#releases`

Create a long-lived branch for that major/feature version:
```
 git checkout -b bX.Y vX.Y.0
 mvn versions:set -DnewVersion=X.Y.1-SNAPSHOT
 git commit -a -m "release branch"
 git push
```

### Quick summary bug fix release

Make a bug fix on the release for the `X.Y`-series:

```
 git checkout bX.Y
 vi NEWS.md
 git commit -m "Update NEWS" NEWS.md
 mvn --batch-mode -DautoVersionSubmodules=true release:clean release:prepare
 git push && git push --tags
```

Log in to Jenkins and run your jobs at [Jenkins](https://jenkins-aws.indexdata.com/job/folio-org/).

[Jira](https://issues.folio.org): Mark as released. Add next versions.

[Slack](https://folio-project.slack.com/): Announce on `#releases`

### Bug fix releases

Generally we want bug fix releases to occur in separate branches with *only* bug fixes (not to be confused with
temporary release branches). For this purpose, we must create a long-lived release branch. We use the naming scheme
`b` followed by the major and minor versions, for example `b2.17` which will include all bug fixes for version 2.17
(so for v2.17.1 and v2.17.2).

The bug fix release can be created as follows. Thus, it happens ONCE after a feature/major release has been performed.

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

### Update platforms if bugfix

If this was a bugfix release, and the platforms need to be updated while waiting for a related UI release, then refer to the [Add to platforms](#add-to-platforms) section below.

### Announce

Send a note to #releases on Slack if relevant.

## Stripes-based modules

All Stripes modules (i.e. `stripes-*` and `ui-*`) follow the
[Stripes release procedure](https://github.com/folio-org/stripes/blob/master/doc/release-procedure.md).

## Add to platforms

### Introduction {#introduction-platform}

This section explains how to update module versions in the platforms (e.g. [platform-core](https://github.com/folio-org/platform-core), [platform-complete](https://github.com/folio-org/platform-complete), etc.) after a new version of a module has been released following the instructions above.
It also explains the related continuous integration process to assist background understanding.

Note that the UI integration tests are now executed on the PR, and that the tests must be passing in order for the module release to be accepted to the FOLIO release.

The [Platform edit steps](#platform-edit-steps) defined below are **mandatory** for module maintainers as part of their role in release management.

### Continuous integration

This is the CI process for a pull-request to master branch or a release branch of a platform. Consider platform-core for example.
The CI stages are defined in its [Jenkinsfile](https://github.com/folio-org/platform-core/blob/master/Jenkinsfile).

The front-end UI modules are declared in
[package.json](https://github.com/folio-org/platform-core/blob/master/package.json) (and installed via 'yarn install') and are declared in the tenant configuration
[stripes.config.js](https://github.com/folio-org/platform-core/blob/master/stripes.config.js) file.
Note that the versions are pinned in package.json (rather than using a comparator) which enables the Renovate bot to discover newer releases ([configured](https://github.com/folio-org/platform-core/blob/master/renovate.json) for platform release branches as "patch" and for master as "minor,patch").

The 'yarn build-module-descriptors' stripes-cli [command](https://github.com/folio-org/stripes-cli/blob/master/doc/commands.md#mod-descriptor-command) processes those declared modules and generates a temporary directory of ModuleDescriptors.
Then a CI script processes those MDs to generate the "stripes-install.json" file.

Then additional modules that are declared in [install-extras.json](https://github.com/folio-org/platform-core/blob/master/install-extras.json) (see explanation below) are appended to that generated [stripes-install.json](https://github.com/folio-org/platform-core/blob/master/stripes-install.json) file.

Then the final stripes-install.json is posted to Okapi `/_/proxy/tenants/diku/install?simulate=true&preRelease=false` to resolve all of the related dependencies, and the output is captured into the [install.json](https://github.com/folio-org/platform-core/blob/master/install.json) file.

Then that "install.json" file is processed to extract the "mod-" ones into the [okapi-install.json](https://github.com/folio-org/platform-core/blob/master/okapi-install.json) file.

After a successful build, the generated artifacts (yarn.lock, install.json, okapi-install.json, stripes-install.json) are committed with message "[CI SKIP] Updating install files on branch".

The link to the built platform "instance" and the link to the "UI Tests" are appended to the PR GitHub page. Note that these will expire after some short time.

### Platform edit steps

To update the version of a module, these steps must be completed.

* Ensure that the module is already being processed on the snapshot branch of the relevant platform.

* If a new `ui-` module is to be added, then declare it in `package.json` and `stripes.install.js` files.

* If a further version constraint is needed, then adjust the `package.json` file.

* As explained in the CI process, Okapi resolves other module dependencies based on those declared UI modules.
If a certain module is not provided by that mechanism (e.g. mod-codex-inventory) then declare it in the `install-extras.json` file.

* Occasionally there is a bugfix release, and the platform needs to be updated while waiting for a related UI release.
So declare that module version in the `install-extras.json` file.

* Submit the PR and ensure proper processing.

Some example PRs:

* [add mod-user-import](https://github.com/folio-org/platform-complete/pull/35)
-- edits `install-extras.json` to add a back-end module that does not get included as a UI dependency.

