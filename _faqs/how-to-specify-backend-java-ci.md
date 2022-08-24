---
layout: page
title: How to specify which Jenkins build image for CI
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 11
---

Back-end Java-based modules can specify which build image to use during the Jenkins continuous integration builds.

For front-end modules that still use Jenkins build rather than GitHub Workflows, the buildNode provides the relevant Nodejs version.

## Using Java 17

For projects that use Java 17:

* In [Jenkinsfile](/guides/jenkinsfile/), declare this in the "buildMvn" section:\
  `buildNode = 'jenkins-agent-java17'`
* In [Jenkinsfile](/guides/jenkinsfile/), declare the mandatory module heath check endpoint via the Docker command `healthChkCmd` to use 'wget'. (There is no 'curl' available on the base image.) 
* In Dockerfile, use:\
  `FROM folioci/alpine-jre-openjdk17:latest`

## Using Java 11

For projects that use Java 11:

* In [Jenkinsfile](/guides/jenkinsfile/), declare this in the "buildMvn" section:\
  `buildNode = 'jenkins-agent-java11'`
* In Dockerfile, use:\
  `FROM folioci/alpine-jre-openjdk11:latest`
* Additional [upgrade notes](https://github.com/folio-org/raml-module-builder/blob/master/doc/upgrading.md#version-310) for projects based on RAML Module Builder (RMB).

## Not using buildMvn pipeline

As some Java-based projects do not use the "buildMvn" pipeline, they can specify the agent node in their Jenkinsfile (either `'jenkins-agent-java17'` or `'jenkins-agent-java11'`) e.g.:

```
agent {
  node {
    label 'jenkins-agent-java11'
  }
}
```

## Node version for front-end

For the few front-end projects that still use Jenkins build rather than GitHub Workflows, the buildNode provides the relevant Nodejs version:

For projects that now use Nodejs 16:

* In [Jenkinsfile](/guides/jenkinsfile/), declare this in the "buildNPM" section:\
  `buildNode = 'jenkins-agent-java17'`

For projects that still use Nodejs 14:

* In [Jenkinsfile](/guides/jenkinsfile/), declare this in the "buildNPM" section:\
  `buildNode = 'jenkins-agent-java11'`

## Using deprecated Java 8

**Note:** FOLIO modules can no longer use the deprecated Java 8 facilities ([FOLIO-2926](https://issues.folio.org/browse/FOLIO-2926)).

<div class="folio-spacer-content"></div>

