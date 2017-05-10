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
    * [Prepare and perform the source release](#prepare-and-perform-the-source-release)
    * [Build and release artifacts ](#build-and-release-artifacts)
    * [Add release notes to GitHub](#add-release-notes-to-github)
    * [Prepare JIRA for next release](#prepare-jira-for-next-release)
    * [Announce](#announce)
    * [Other current Maven-related discussion](#other-current-maven-related-discussion)
* [Stripes-based modules](#stripes-based-modules)
    * [Other current Stripes-related discussion](#other-current-stripes-related-discussion)

## Introduction

There are separate notes about the
[FOLIO version-numbering scheme](http://dev.folio.org/community/contrib-code#version-numbers).

## Maven-based modules

The procedure is outlined here for "Okapi" and is similar for other Maven-based modules.

### Ensure POM declarations

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
Maven 'deploy' phase should have the following specified in the project's top-level POM:

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
    <url>https://github.com/folio-org/PROJECT_NAME</url>
    <connection>scm:git:git://github.com/folio-org/PROJECT_NAME.git</connection>
    <developerConnection>scm:git:git@github.com:folio-org/PROJECT_NAME.git</developerConnection>
    <tag>HEAD</tag>
  </scm>
```

Replace 'PROJECT_NAME' above with the name of the appropriate github repository.  
Commit all changes to the POM in git. 


### Ensure that JIRA issues are ready

For the issues that are associated with this release, ensure that they reflect reality,
have the relevant `Fix Version` parameter, and are closed.

### Prepare the news document

Edit `NEWS.md` to add concise descriptions and issue numbers for each major item.
Take extra care with spelling and readability.

```
git commit -m "Update NEWS" NEWS.md
```

### Prepare and perform the source release 

```
mvn -DautoVersionSubmodules=true release:clean release:prepare
```
This command will prompt you for input including the release tag/version,
the next, post-release SNAPSHOT version, as well as ask you to resolve
any SNAPSHOT dependencies if you have any (Do NOT create releases with
SNAPSHOT dependencies!).  Selecting the defaults are typically fine.  
Your release tag should always be prefixed with 'v' (the default) and you can 
always change the next SNAPSHOT version later if necessary.

Assuming there are no build errors, you are ready to push your changes to
GitHub. 

```
git push
git push --tags
```

### Build and release artifacts

An 'artifact' in this context could either be an Maven artifact released to the FOLIO 
Maven repository, a docker image released to Docker Hub, a Linux distribution package
or some combination of artifacts depending on the project.  To release the artifacts 
relevant to your project, log into the [FOLIO Jenkins system](https://jenkins-aws.indexdata.com).
Navigate to your project's folder and select the Jenkins job name with the '-release' suffix.
For example, 'okapi-release'.   Select 'Build with Parameters' and select the release tag you
want to release.  This will build the release artifacts and deploy them to the proper
repositories.


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

## Stripes-based modules

All Stripes modules (i.e. stripes-* and ui-*) follow the
[Stripes release procedure](https://github.com/folio-org/stripes-core/blob/master/doc/release-procedure.md).

### Other current Stripes-related discussion

* [STRIPES-309](https://issues.folio.org/browse/STRIPES-309)
  -- Align git-repos, NPM-packages and Jira projects for Stripes and UI modules.
