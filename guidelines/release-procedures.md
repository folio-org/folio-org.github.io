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
* [Regular releases](#regular-releases)

## Introduction

There are separate notes about the
[FOLIO version-numbering scheme](/guidelines/contributing/#version-numbers)
and the [Build, test, and deployment infrastructure](/guides/automation/).

## Maven-based modules

The procedure is outlined here for "Okapi" and is similar for other back-end Maven-based modules.

Please follow all steps in a timely manner, i.e. do not follow some steps one day and the rest the next day, as that will lead to broken systems.

### Quick summary major/feature release {#summary-mvn}

(However follow this complete document for its important information.)

In this example we are releasing `X.Y.0` of a module.

```
 git checkout -b tmp-release-X.Y.0
 vi NEWS.md
 git commit -m "Update NEWS" NEWS.md
 mvn -DautoVersionSubmodules=true release:clean release:prepare # Supply next feature (X.Y+1.0-SNAPSHOT)
 git push && git push --tags
 mvn release:clean
```
Log in to Jenkins and run your jobs at [Jenkins](https://jenkins-aws.indexdata.com/job/folio-org/).

[GitHub](https://github.com/folio-org): Merge temporary release branch `tmp-release-X.Y.0` to mainline,
after [Verify increment POM version mainline](#verify-increment-pom-version-mainline).

[Jira](https://folio-org.atlassian.net/jira): Mark as released. Add next versions.

[Slack](https://folio-project.slack.com/): Announce on `#folio-releases`

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

[Jira](https://folio-org.atlassian.net/jira): Mark as released. Add next versions.

[Slack](https://folio-project.slack.com/): Announce on `#folio-releases`

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

For Maven-based projects, the [Maven Release Plugin](https://maven.apache.org/maven-release/maven-release-plugin)
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
descriptors from [templates](/guides/commence-a-module/#back-end-descriptors).
Note that scripts can enable the module without mentioning any version numbers.

Commit any such changes:

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
For example `2.18.0-SNAPSHOT` rather than `2.17.1-SNAPSHOT` version.
Refer to additional explanation in the [next](#ensure-increment-pom-version-mainline) section.

Assuming there are no build errors, then you are ready to push your changes to
GitHub and delete the release.properties and pom.xml.releaseBackup files.

```
git push && git push --tags
mvn release:clean
```

### Ensure increment POM version mainline

Regarding the previous step, it is vitally important for continuous integration that the POM version on mainline branch is incremented to the next minor version.
Essentially that version must be greater than any released version.
Otherwise CI will use outdated snapshot versions and lead to undesired consequences (which can also be failed builds and hence disruption for the whole FOLIO project).

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
Jenkins credentials utilize the GitHub authentication for FOLIO developers, so ensure that you are logged in to GitHub to then enable login to Jenkins.

Select the [GitHub folio-org](https://jenkins-aws.indexdata.com/job/folio-org/) folder, then follow to the relevant job (e.g.
[mod-circulation](https://jenkins-aws.indexdata.com/job/folio-org/job/mod-circulation/)) and select the "Tags" tab. Select the new release version tag, then the "Build Now" link in the left-hand panel to trigger it.

### Verify increment POM version mainline

Before doing the merge in the next step, be absolutely sure that the POM version will be appropriately incremented as described in the [earlier](#ensure-increment-pom-version-mainline) steps.

### Merge the temporary release branch into master

Before proceeding, verify the [previous](#verify-increment-pom-version-mainline) step.

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

Send a note to #folio-releases channel on Slack.

## Stripes-based modules

All Stripes modules (i.e. `stripes-*` and `ui-*`) follow the
[Stripes release procedure](https://github.com/folio-org/stripes/blob/master/doc/release-procedure.md).

## Add to platforms

### Introduction {#introduction-platform}

Currently there are two repositories maintained by the FOLIO project that bundle together UI and backend modules into a compatible set of FOLIO modules.

* [platform-complete](https://github.com/folio-org/platform-complete) - The complete set of frontend and backend FOLIO modules
* [platform-minimal](https://github.com/folio-org/platform-minimal) - A "minimal" set of frontend and backend FOLIO modules

Each of these repositories contain configurations and tools to build a Stripes bundle as well as files that list a set of compatible backend modules.

### Descriptions of key files

* package.json  - This NPM file specifies a list of FOLIO stripes and UI modules and additional NPM dependencies needed to build a Stripes webpack.
* stripes.config.js - Stripes-specific configuration file. If your UI module is a FOLIO app and contains a module descriptor, it should be added to this file.
* install.json - This file contains a json-formatted list of all FOLIO modules that comprise the platform.   It is automatically generated by CI and **should not be edited directly**.  This is the complete list of modules that can enabled for a tenant using Okapi's '`/_/proxy/tenants/TENANT/install`' endpoint.
* okapi-install.json - This file is also automatically generated by CI and **should not be edited directly**.  It describes a subset of modules in the platform that Okapi should deploy when utilizing Okapi in deployment mode.
* stripes-install.json - This file is automatically generated by CI and **should not be edited directly**.  It describes a subset of modules in the platform that can be enabled for a tenant but are not deployed by Okapi (when utilizing Okapi's deployment functionality).
* install-extras.json - This file contains a list of backend modules that are not dependencies of any UI modules but should be included in the platform. This list can be edited.

The most typical operations in these repositories involve changes to 'package.json', 'stripes.config.js', and 'install-extras.json' files.
(**Note**: The 'install.json', 'okapi-install.json', and 'stripes-install.json' files are generated by FOLIO CI.  They should almost **never be edited** by a user directly.)

### Descriptions of key branches

Each platform repository has three kinds of protected, long-term branches:

* 'master' branch - This branch represents the most up-to-date set of compatible, released FOLIO modules.
* 'snapshot' branch - This branch represents the most up-to-date set of compatible, unreleased ("snapshots") FOLIO modules.
* release branch (e.g. 'R2-2024') - These branches represent a set of compatible, released FOLIO modules that have passed user-acceptance testing. This is typically the most stable branch of the FOLIO platform.

Each of these branches is managed in similar, although not entirely identical ways.
The master and release branches contain sets of FOLIO modules that are pinned to specific released versions.
The snapshot branch, on the other hand, is generally configured to get the latest versions of unreleased, compatible modules.

### Continuous integration

This is the CI process for a pull-request to master branch or a release branch of a platform. Consider platform-complete for example.
The CI stages are defined in its [Jenkinsfile](https://github.com/folio-org/platform-complete/blob/master/Jenkinsfile).

As noted previously, FOLIO modules are pinned to released versions.
A dependency bot called Renovate is [configured](https://github.com/folio-org/platform-complete/blob/master/renovate.json) to discover new, individual FOLIO frontend and backend module releases that are compatible with each branch of the platform.
Specifically, the bot examines 'package.json' and 'install-extras.json' and compares the versions of modules listed in these files with the latest releases in the FOLIO NPM and Docker repositories.
For the release branches, Renovate is configured to scan for newer patch releases.
For the master branch, Renovates compares minor and patch releases.
In both cases, Renovate will automatically create pull-requests to those platform branches for each compatible release that it detects.  PRs issued by Renovate are not automatically merged.  They still require developers or devops to approve and merge.

The 'yarn build-module-descriptors' stripes-cli [command](https://github.com/folio-org/stripes-cli/blob/master/doc/commands.md#mod-descriptor-command) processes those declared modules and generates a temporary directory of ModuleDescriptors.
Then a CI script processes those MDs to generate the "stripes-install.json" file.

Then additional modules that are declared in [install-extras.json](https://github.com/folio-org/platform-complete/blob/master/install-extras.json) (see explanation below) are appended to that generated [stripes-install.json](https://github.com/folio-org/platform-complete/blob/master/stripes-install.json) file.

Then the final stripes-install.json is posted to Okapi `/_/proxy/tenants/diku/install?simulate=true&preRelease=false` to resolve all of the related dependencies, and the output is captured into the [install.json](https://github.com/folio-org/platform-complete/blob/master/install.json) file.

Then that "install.json" file is processed to extract the "mod-" ones into the [okapi-install.json](https://github.com/folio-org/platform-complete/blob/master/okapi-install.json) file.

After a successful build, the generated artifacts (yarn.lock, install.json, okapi-install.json, stripes-install.json) are committed with message "[CI SKIP] Updating install files on branch".  Do not manually edit those files -- they are autogenerated by Jenkins.

The link to the built platform "instance" and the link to the "UI Tests" are appended to the PR GitHub page. Note that these will expire after some short time.

### Manage master and release branches

This section explains how and when to manage modules in the platforms (e.g. [platform-complete](https://github.com/folio-org/platform-complete)) after a new version of a module has been released.
There are cases when Renovate will not update modules automatically, so changes to the platform will need to be done manually.  These cases include the following:

* A new UI module needs to be included in the platform.  Before adding a new module to the platform, ensure that the module has already been added and tested on the snapshot branch and included in the  [snapshot](/faqs/how-to-install-new-module/) reference environments.
Add the new UI module and specify the version in 'package.json'.  Add the module to 'stripes.config.js' (if appropriate).

* A new backend module needs to be included in the platform, and it is NOT a dependency of any of the UI modules that are listed in the platform's package.json file.
In these cases, the module should be added to the 'install-extras.json' file.
As with new UI modules, ensure that the module has already been added and tested on the snapshot branch and included in the  [snapshot](/faqs/how-to-install-new-module/) reference environments.

* A new major release needs to be added to the master branch of the platform to either 'package.json' or 'install-extras.json' files.

* A new major or minor release needs to be added to a release branch of the platform to either 'package.json' or 'install-extras.json' files.

Before opening any new pull requests in either platform repository, create your own local branch of the master or release branch, and push the branch to the appropriate platform repository.
Pushing the local branch to GitHub is mandatory before issuing a new PR -- so ensure that you have commit privileges.

As explained [above](#continuous-integration), during the CI process Okapi resolves other module dependencies based on those declared UI modules, and on modules that are listed in the 'install-extras.json' file.
So not every backend module will be listed in the 'install-extras.json' file.
There is an exception to this rule. Once an intial release branch is finalized, all backend modules are pinned in the 'install-extras.json' file.
This ensures that only new patch-level backend module releases are updated on release branches.

Once the changes in your branch are being properly processed by CI, then submit the PR and ensure its proper processing.
Seek a PR review before merging to your target branch.

Some example PRs:

* [add mod-user-import](https://github.com/folio-org/platform-complete/pull/35)
-- edits `install-extras.json` to add a back-end module that does not get included as a UI dependency.

## Regular releases

In addition to the normal release steps explained above, there are some additional steps at the time of [Regular FOLIO releases](/guides/regular-releases/).

Be aware of the upcoming release dates and cut-off times.

Follow the module co-ordination spreadsheets, and keep the information entries for your modules up-to-date.

Ensure the accuracy of any "community release notes" for your modules.

