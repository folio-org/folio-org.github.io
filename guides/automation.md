---
layout: page
title: Build, test, and deployment infrastructure
permalink: /guides/automation/
menuInclude: no
menuTopTitle: Guides
---

## Overview

This document describes the implementation, processes, and automated workflow for
FOLIO projects maintained in the [folio-org GitHub](/source-code) repositories.
The [release procedures](/guidelines/release-procedures/) are separately summarised.

The build, test, release, and deployment processes are, in large part, orchestrated and
automated by Jenkins.  A Nexus repository is used to host FOLIO Maven artifacts and
NPM packages, and Docker Hub is used as the Docker registry for Docker images.  AWS
provides the infrastructure used to host Jenkins and Nexus, as well as permanent and
on-demand resources for FOLIO integration testing and demos.

## Software build pipeline

<img src="/images/FOLIO-Software-Build-pipeline.png" alt="FOLIO Software Build Pipeline" srcset="/images/FOLIO-Software-Build-pipeline.svg">
<!-- The source of this SVG is an OmniGraffle file in work/graphic-source/ -->

The project is using a continuous integration -- or CI -- system (described below) that builds new versions of the software whenever a developer makes a change, as well as on a timed basis.
The CI system automatically builds reference environments that are used for various purposes by the developers, the product owners, and the testers.

In order to fully understand this diagram, keep in mind that there are two parts to FOLIO -- the part called “Stripes” which is the software running in the browser and the part called “Okapi” which is running on the server.

The Okapi backend is secured during the CI process. For more information on securing Okapi see the [folio-install](https://github.com/folio-org/folio-install/blob/master/runbooks/single-server/README.md#secure-the-okapi-api-supertenant) and the [guide on securing Okapi](https://github.com/folio-org/okapi/blob/master/doc/securing.md).
Default settings for securing okapi are in the okapi-secure Ansible role's [defaults](https://github.com/folio-org/folio-ansible/blob/master/roles/okapi-secure/defaults/main.yml) file.
Direct access is via URLs such as [https://folio-testing-okapi.aws.indexdata.com](https://folio-testing-okapi.aws.indexdata.com/)

Another part that is not indicated in this diagram are various "edge" modules, which bridge the gap between some specific third-party services and FOLIO (e.g. RTAC, OAI-PMH).
On these FOLIO reference environments, the set of edge services are accessed via port 8000.
The API key is explained at [edge-common](https://github.com/folio-org/edge-common#security).
The edge APIs are deployed such that any API key generated with the tenant diku and institutional user diku will work (ephemeral secure store is being used which ignores the salt portion of the key).

## Reference environments

Each environment listed below is based on the [platform-complete](https://github.com/folio-org/platform-complete) Stripes Platform.
Each also has one based on [platform-core](https://github.com/folio-org/platform-core), so adjust the link to include `-core` (e.g. `folio-testing` to `folio-testing-core`).
Similarly okapi can be accessed via `folio-testing-okapi` (and see notes in the previous section).

If an error message (in the 5** series) is shown for the entry point of these sites, then that probably means that it is in the process of being rebuilt (see its "Jenkins job" link).

### folio-testing

[https://folio-testing.aws.indexdata.com/](https://folio-testing.aws.indexdata.com/)

The frontend (Stripes) is rebuilt every even two hours, to finish about 10 minutes past (see Jenkins job: [folio-testing-stripes](https://jenkins-aws.indexdata.com/job/Automation/job/folio-testing-stripes/)).
The backend (Okapi + modules) is built every day, to finish about 01:45 UTC (see Jenkins job: [folio-testing-backend](https://jenkins-aws.indexdata.com/job/Automation/job/folio-testing-backend/)).

The set of frontend modules are those listed in the "snapshot" branch of the Stripes Platform.
The frontend build consists of the master branch of each frontend module at that time.

The set of backend modules is a list explicitly declared in folio-ansible.
The backend build consists of the master branch of each backend module at that time.
There is no attempt to verify that the frontend dependencies are met by the backend modules, so there may be errors caused by that mismatch.

### folio-snapshot

[https://folio-snapshot.aws.indexdata.com/](https://folio-snapshot.aws.indexdata.com/)

Built every day, to finish about 03:50 UTC (see Jenkins job: [folio-snapshot](https://jenkins-aws.indexdata.com/job/Automation/job/folio-snapshot/)).

The set of frontend modules are those listed in the "snapshot" branch of the Stripes Platform.

This build consists of the master branch of each frontend module at that time, paired with the latest version of backend modules that meet the dependency requirements of the frontend.
There may still be errors because of API differences that aren't covered by the dependency requirements.
The folio-snapshot is an alias for folio-snapshot-latest.

### folio-snapshot-stable

[https://folio-snapshot-stable.aws.indexdata.com/](https://folio-snapshot-stable.aws.indexdata.com/)

After `folio-snapshot` is built, the CI system runs a suite of integration and regression tests.
This phase normally takes about 10 minutes, but sometimes reaches a timeout of about 1 hour.
If those tests pass, the `folio-snapshot-stable` alias is updated to point to this latest `folio-snapshot` version.
This is the version that will be used by acceptance testers to verify that users stories are completed.

### folio-snapshot-load

[https://folio-snapshot-load.aws.indexdata.com/](https://folio-snapshot-load.aws.indexdata.com/)

When doing any substantial test data loading, then use this rather than the other systems.
This the same as "folio-snapshot".
The server is built every day, to finish about 02:00 UTC (see Jenkins job: [folio-snapshot-load](https://jenkins-aws.indexdata.com/job/Automation/job/folio-snapshot-load/)).

### folio-release

[https://folio-release.aws.indexdata.com/](https://folio-release.aws.indexdata.com/)

Built every day, to finish about 01:30 UTC (see Jenkins job: [folio-release](https://jenkins-aws.indexdata.com/job/Automation/job/folio-release/)).

The set of frontend modules are those listed in the "master" branch of the Stripes Platform.
The set of backend modules are those determined as dependencies of the frontend (plus some explicit extras).

This build uses the latest compatible releases of each module, i.e. using only released versions of the software (no snapshots).
It is a running preview of released code, leading up to the next quarterly release.

### folio-daisy

[https://folio-daisy.aws.indexdata.com/](https://folio-daisy.aws.indexdata.com/)

This is an environment for the most recent FOLIO Release Q3 2019 Daisy.
Each nightly rebuild will pick up any hotfix updates that may have been released.
Built every day, to finish about 03:30 UTC (see Jenkins job: [folio-q3.2-2019-release](https://jenkins-aws.indexdata.com/job/Automation/job/folio-q3.2-2019-release/)).

### Other notes

The software versions of each module is shown via the system settings,<br/>
e.g. [https://folio-snapshot.aws.indexdata.com/settings/about](https://folio-snapshot.aws.indexdata.com/settings/about)

The frontend and backend module versions are listed in `okapi-install.json`, `stripes-install.json` and `yarn.lock`
(see [explanation](/guidelines/release-procedures/#add-to-platforms) of how those resource files are generated by the CI process).
For example:<br/>
[https://folio-snapshot-stable.aws.indexdata.com/okapi-install.json](https://folio-snapshot-stable.aws.indexdata.com/okapi-install.json)<br/>
[https://folio-snapshot-stable.aws.indexdata.com/stripes-install.json](https://folio-snapshot-stable.aws.indexdata.com/stripes-install.json)<br/>
[https://folio-snapshot-stable.aws.indexdata.com/yarn.lock](https://folio-snapshot-stable.aws.indexdata.com/yarn.lock)

## Jenkins

FOLIO projects are managed by the Jenkins host [https://jenkins-aws.indexdata.com](https://jenkins-aws.indexdata.com)
located at AWS.  Read access to Jenkins job configurations and build logs is available to
all core FOLIO developers.
Jenkins credentials utilize the Github authentication, so ensure that you are logged in to GitHub to then enable log in to Jenkins.

See [Navigation of commits and CI via GitHub and Jenkins](/guides/navigate-commits/).

A standard Jenkins build job configuration for a GitHub project consists roughly
of the following steps: a git clone of the GitHub project repository's master branch,
a build step, post-build steps such as creating and publishing docker images, and
post-build notifications to GitHub and Slack (#folio-ci channel).
Failures and unstable build notifications are also sent via e-mail.

Those extra build steps are configured in the project's repository in a file called `Jenkinsfile`
which is separately [explained](/guides/jenkinsfile/).

Each FOLIO software project will also have a separate Jenkins job configured to
rebuild branches and build pull requests.  The status of these is posted back to GitHub and Slack.

Utilizing pull requests to verify that your development branch builds properly before
merging with master is required.

Occasionally there might be a need to trigger Jenkins to re-run a job.
So log in to Jenkins as described above, and find the relevant Automation job.
If you have the permissions to do so, then the job can be initiated.

Another common Jenkins job is dedicated to code releases.
See [release procedures](/guidelines/release-procedures/).

Also refer to the [explanation](/guidelines/release-procedures/#add-to-platforms) of Jenkins handling of PRs for Stripes Platforms, and the use of Renovate bot.

Other Jenkins automation jobs exist as well for test deployments to AWS EC2 instances.

## Monitoring and performance

Various facilities are available:

* [Performance report](https://jenkins-aws.indexdata.com/job/Automation/job/folio-perf-test/) to monitor throughput, response times, error rates, etc.
The tests are configured in the [folio-perf-test](https://github.com/folio-org/folio-perf-test) repository, and utilise Apache JMeter.
Runs once per day.
* [FOLIO Environment Dashboard](https://dashboard.folio.ebsco.com/).

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

Docker images are published to the ['folioci' namespace on Docker Hub](https://hub.docker.com/r/folioci).
This namespace is primarily used by Jenkins for other continuous
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

A separate set of repositories on Docker Hub are designated for "released"
versions of modules: the ['folioorg' namespace](https://hub.docker.com/r/folioorg).

Docker Hub repository permissions are very similar to GitHub's repository permissions.
It is possible to invite Docker Hub users to collaborate on repositories within
the namespace on a per repository basis.
