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
Direct access is via URLs such as `https://folio-snapshot-okapi.dev.folio.org`

Another part that is not indicated in this diagram are various "edge" modules, which bridge the gap between some specific third-party services and FOLIO (e.g. RTAC, OAI-PMH).
On these FOLIO reference environments, the set of edge services are accessed via port 8000.
The API key is explained at [edge-common](https://github.com/folio-org/edge-common#security).
The edge APIs are deployed such that any API key generated with the tenant diku and institutional user diku will work (ephemeral secure store is being used which ignores the salt portion of the key).

## Reference environments

### Explanation

Each environment listed below is based on the [platform-complete](https://github.com/folio-org/platform-complete) Stripes Platform.
<!-- Awaiting platform-minimal:
Each also has one based on [platform-core](https://github.com/folio-org/platform-core), so adjust the link to include `-core` (e.g. `folio-snapshot` to `folio-snapshot-core`).
Similarly okapi can be accessed via `folio-snapshot-core-okapi` (and see notes in the previous section).
-->

The folio-snapshot and folio-snapshot-2 are constructed identically every 24 hours, with a 12-hour offset.
There are also two [flower release](/guides/regular-releases/) environments (the current and the previous) which are rebuilt weekly on a Sunday.

The environments are completely torn-down and rebuilt again.

If an error message (in the 5** series) is shown for the entry point of these sites, then that probably means that it is in the process of being rebuilt (see its "Jenkins job" link).

(There is also the Wiki page [Reference environments](https://folio-org.atlassian.net/wiki/spaces/FOLIJET/pages/513704182/Reference+environments) which lists some other environments related to ECS and Eureka.)

### Developer scratch environments

Team-specific testing and development does not happen on these reference environments.
Instead use the dedicated Rancher [scratch environments](/faqs/how-to-get-started-with-rancher/).
These can be configured and scaled specifically to meet the needs of particular teams and POs, e.g. to allow for large datasets, etc.

### Off-schedule rebuilds

DevOps will not accept requests for manual rebuilds of either environment unless special or unusual circumstances dictate otherwise.
If a team needs to confirm an updated module, then await the next scheduled 12-hourly run.

If there is an **urgent** need to re-run a build outside of the normal automation schedule (explained below),
then co-ordinate that on the Slack channel #folio-hosted-reference-envs
(remember that there are other people utilising these systems).

<a id="install-json"></a>Also, as [explained](#platform-hourly-build) below, before doing this wait for the automated hourly build of the “snapshot” branch of the Stripes Platform and ensure that the expected module versions are included
in that build's automatically generated [install.json](https://github.com/folio-org/platform-complete/blob/snapshot/install.json) file.
Correlate the "build number" with that shown in the output log of the project's "Publish module descriptor" stage.

### Troubleshooting

Failures with the main builds are automatically sent to the `#folio-hosted-reference-envs` Slack channel.

Follow its links to the Jenkins job output.

Refer to the FAQs
[How to obtain reference environment module logs](/faqs/how-to-obtain-refenv-logs/)
and
[How to investigate Jenkins build logs](/faqs/how-to-investigate-jenkins-logs/).

For failed [Platform hourly build](#platform-hourly-build) jobs, the Okapi log is linked from the left-hand panel of its Jenkins job summary page.

As noted in the [Platform hourly build](#platform-hourly-build) section below, it is vitally important that developers ensure success of the subsequent hourly build following any major changes that they merge to mainline (especially on a Friday afternoon). Continued failures of this hourly job will cause the “folio-snapshot” builds to use out-of-date install files.

### folio-snapshot

[https://folio-snapshot.dev.folio.org/](https://folio-snapshot.dev.folio.org/)

The server is built every day, to finish about 02:03 UTC.\
(See Jenkins job: [folio-snapshot](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot/) which starts about 01:24 UTC.).

#### Included module versions

The folio-snapshot builds consist of the master branch of each frontend module at that time, paired with the latest version of backend modules that meet the dependency requirements of the frontend (as determined by the preceding [hourly platform build](#platform-hourly-build)).
There may still be errors because of API differences that aren't covered by the dependency requirements.

### folio-snapshot-2

[https://folio-snapshot-2.dev.folio.org/](https://folio-snapshot-2.dev.folio.org/)

This is constructed in the same manner as "folio-snapshot" (see its [explanation](#folio-snapshot)), but approximately 12-hours later.

The server is built every day, to finish about 14:00 UTC.\
(See Jenkins job: [folio-snapshot-2](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-snapshot-2/) which starts about 13:21 UTC.)

The folio-snapshot-latest is an alias for folio-snapshot-2.

### Platform hourly build

The set of frontend modules are those listed in the "snapshot" branch of the Stripes Platform.

The "snapshot" branch of the Stripes Platform is rebuilt every hour, starting about 19 minutes past the hour and finishing about 50 minutes past (see Jenkins job: [build-platform-complete-snapshot](https://jenkins-aws.indexdata.com/job/Automation/job/build-platform-complete-snapshot/)).
If successful, then this will [regenerate](/guidelines/release-procedures/#add-to-platforms) the yarn.lock and install files of the Platform (see [note above](#install-json)), to be utilised by the abovementioned "folio-snapshot" job.
So if there is an urgent need to [rebuild](#off-schedule-rebuilds) "folio-snapshot" outside of normal automation, so as to include a new snapshot of a module, then this build needs to have run before the "folio-snapshot" build is re-run.

It is vitally important that developers ensure success of the subsequent hourly build following any major changes that they merge to mainline (especially on a Friday afternoon). As noted in the previous paragraph, failures of this hourly job will cause the "folio-snapshot" builds to use out-of-date install files.
Refer to the [Troubleshooting](#troubleshooting) assistance section above.

### folio-ramsons

[https://folio-ramsons.dev.folio.org/](https://folio-ramsons.dev.folio.org/)

This is an environment for the previous FOLIO Release R2 2024 Ramsons.
Each rebuild will pick up any hotfix updates that may have been released.

The server is deliberately not being automatically re-built each week,
while a PC Working Group is gathering better sample data for the reference environments.\
(See Jenkins job: [folio-r2-2024-release](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-r2-2024-release/).)

### folio-quesnelia

[https://folio-quesnelia.dev.folio.org/](https://folio-quesnelia.dev.folio.org/)

This is an environment for the previous FOLIO Release R1 2024 Quesnelia.
Each rebuild will pick up any hotfix updates that may have been released.

The server is deliberately not being automatically re-built each week,
while a PC Working Group is gathering better sample data for the reference environments.\
(See Jenkins job: [folio-r1-2024-release](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-r1-2024-release/).)

### Other notes

The software versions of each module is shown via the system settings,\
e.g. [https://folio-snapshot.dev.folio.org/settings/about](https://folio-snapshot.dev.folio.org/settings/about)

The frontend and backend module versions are listed in `okapi-install.json` and `stripes-install.json` and `yarn.lock`
(see [explanation](/guidelines/release-procedures/#add-to-platforms) of how those resource files are generated by the CI process).
For example:\
[https://folio-snapshot.dev.folio.org/okapi-install.json](https://folio-snapshot.dev.folio.org/okapi-install.json)\
[https://folio-snapshot.dev.folio.org/stripes-install.json](https://folio-snapshot.dev.folio.org/stripes-install.json)\
[https://folio-snapshot.dev.folio.org/yarn.lock](https://folio-snapshot.dev.folio.org/yarn.lock)

The [FTP CI test server](/guides/ftp-ci-server/) is available to verify FTP operations for various applications, e.g. Acquisitions.

## Jenkins

FOLIO projects are managed by the Jenkins host [https://jenkins-aws.indexdata.com](https://jenkins-aws.indexdata.com)
located at AWS.  Read access to Jenkins job configurations and build logs is available to
all FOLIO developers.
Jenkins credentials utilize the Github authentication, so ensure that you are logged in to GitHub to then enable login to Jenkins.

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

* [Performance report](https://jenkins-aws.indexdata.com/job/FOLIO_Reference_Builds/job/folio-perf-test/) to monitor throughput, response times, error rates, etc.
The tests are configured in the [folio-perf-test](https://github.com/folio-org/folio-perf-test) repository, and utilise Apache JMeter.
Runs once per day.

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

Typically, this can be set via one of the following NPM commands:

```
npm config set registry https://repository.folio.org/repository/npm-folio/
```

```
npm config set registry https://repository.folio.org/repository/npm-folioci/
```

Deployment to the FOLIO repositories requires the proper permission. Artifacts
and packages should only be deployed to the FOLIO Maven and NPM repositories via a
build job configured in Jenkins.

`npm-folio` is where the formal release artefacts of UI modules are published to.
These are used to build the official distributions of FOLIO e.g. 2020 Q3 - Honeysuckle.
These artefacts are produced by dedicated release builds.

`npm-folioci` is where the pre-release artefacts are published to. They are sometimes
referred to as “tip-of-master” because any time a PR is merged to the master branch of
a UI module, a new artifact is automatically published to npm-folioci.
These are used for building the hosted reference environments for testing purposes e.g.
https://folio-snapshot.dev.folio.org/ . These artefacts are produced by the
mainline (usually named master) builds for each module.

Most developers are working on pre-release versions of the software and so want to
check it works with other pre-release versions of other libraries/modules rather
than the last formally released version which could be a few months old.

## Docker Hub

Docker images are the primary distribution model for FOLIO modules.  All modules
should include a Dockerfile that describes how to build a runtime Docker image for the
module.  If a Dockerfile is present, Jenkins will create a Docker image for the module
and publish the image to a repository on Docker Hub as a post-build step if the previous
build step is successful.
That CI stage also deploys a Docker Hub README [generated](/guides/module-descriptor#docker-hub-readme) from the LaunchDescriptor.

Docker images are published to the ['folioci' namespace on Docker Hub](https://hub.docker.com/u/folioci).
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
versions of modules: the ['folioorg' namespace](https://hub.docker.com/u/folioorg).

Docker Hub repository permissions are very similar to GitHub's repository permissions.
It is possible to invite Docker Hub users to collaborate on repositories within
the namespace on a per repository basis.
