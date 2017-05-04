---
layout: page
title: Build, test, and deployment infrastructure
---

## Overview

This document describes the implementation, processes, and automated workflow for
FOLIO projects maintained in the [folio-org GitHub](../source-code) repositories.

The build, test, release, and deployment processes are, in large part, orchestrated and
automated by Jenkins.  A Nexus repository is used to host FOLIO Maven artifacts and
NPM packages, and Docker Hub is used as the Docker registry for Docker images.  AWS
provides the infrastructure used to host Jenkins and Nexus as well permanent and
on-demand resources for FOLIO integration testing and demos.

## Jenkins

FOLIO projects are managed by the Jenkins host, https://jenkins-aws.indexdata.com
located at AWS.  Read access to Jenkins job configurations and build logs is available to
all core FOLIO developers.  Credentials are required.

A standard Jenkins build job configuration for a Github project consists roughly
of the following steps: a git clone of the GitHub project repository's master branch,
a build step, post-build steps such as creating and publishing docker images, and
post-build notifications to GitHub and Slack (Index Data #bot-jenkins channel).
Failures and unstable build notifications are also sent via e-mail.

Each FOLIO software project may also have a separate Jenkins job configured to
build GitHub pull requests.  The status of the pull request is posted back to GitHub,
so utilizing pull requests to verify that your development branch builds properly before
merging with master is highly recommended.

Another common Jenkins job is dedicated to code releases.  For Maven-based projects, the
Maven Release Plugin is required.  To enable the release plugin, add the following to
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

These jobs are initiated manually and parameterized.  The two primary parameters
are the release version and the next development version.

```
mvn release:clean release:prepare release:perform \
  -DreleaseVersion=${releaseVersion} -DdevelopmentVersion=${developmentVersion}
```

Together, Jenkins and Maven perform roughly the following steps to coordinate a release:

* Local 'git checkout' of the master branch of the project from GitHub.
* Check that there are no SNAPSHOT dependencies.
* Run build and unit tests on current branch to ensure build is stable.
* Update parent and child POMs to $releaseVersion, tag the release, make local commits.
* Update parent and child POMs to $developmentVersion and locally commit.
* Local git checkout of release tag, and perform release build and deploy Maven artifacts
  to Maven release repository (if specified).
* Run any post-build steps such as building and publishing Docker images and running
  additional integration tests.
* If all build and post-build steps complete successfully, the last step is to have
  Jenkins push all commits and tags back to the master branch of the project repository
  on GitHub.  If any part of this process fails, no tags or commits are pushed
  to the origin repository.

Other Jenkins automation jobs exist as well for test deployments to AWS EC2 instances.

## Nexus Repository Manager

FOLIO utilizes the Nexus OSS Repository Manager to host [Maven artifacts and
NPM packages](https://repository.folio.org) for FOLIO projects.

The hosted FOLIO Maven repositories consist of two distinct repos - a snapshot
and release repository.  A 'mvn deploy' will automatically deploy artifacts to
the proper repository depending on the project version specified in the POM.
Only Jenkins has deployment permissions to these repositories.  However, they are
available "read-only" to the FOLIO development community.  FOLIO Maven projects that
depend on Maven artifacts from other FOLIO projects can retrieve the artifacts by
specifying the following in the project's POM:

```xml
  <repositories>
    <repository>
      <id>folio-nexus</id>
      <name>FOLIO Maven repository</name>
      <url>https://repository.folio.org/repository/maven-folio</url>
    </repository>
  </repositories>
```

The URL will search both the snapshot and release repositories for the artifact
specified.

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
```

Node.js-based FOLIO projects can either deploy or retrieve FOLIO NPM
dependencies by adding the location of the FOLIO NPM repository to their
NPM settings.

Typically, this can be set via the following NPM command:

```
npm config set registry https://repository.folio.org/repository/npm-folio/
```

Deployment to the FOLIO repositories requires the proper permission. Artifacts
and packages should only be deployed to the FOLIO Maven and NPM repositories via a
build job configured in Jenkins.

## Docker Hub

Docker images are the primary distribution model for FOLIO modules.  All modules
should include a Dockerfile that describes how to build a runtime Docker image for the
module.  If a Dockerfile is present, Jenkins will create a Docker image for the module
and publish the image to a repository on Docker Hub as a post-build step if the previous
build step is successful.

Presently, Docker images are published to the ['folioci' namespace on Docker Hub](https://hub.docker.com/r/folioci).  This namespace is primarily used by Jenkins for other continuous
integration jobs but is also open to the FOLIO development community for testing and
development purposes.  "Snapshot" versions of modules are published after every
successful Jenkins build.   To pull an image from the 'folioci' namespace, prefix the
module name with 'folioci'.

For example:

```
docker pull folioci/mod-circulation:latest
```

Images are currently tagged with the current version of the module as well as with
'latest' which designates the most recent version.  Alternative tagging methods may
include the Jenkins build number, git commit ID, or git tag.  Similar to the Maven
repositories, write access to the 'folioci' repositories is via Jenkins only.

A separate set of repositories on Docker Hub will be designated for "released"
versions of modules and will either reside in the TBD 'folio' or 'folioorg' namespace
on Docker Hub.

Docker Hub repository permissions are very similar to GitHub's repository permissions.
It is possible to invite Docker Hub users to collaborate on repositories within
the namespace on a per repository basis.
