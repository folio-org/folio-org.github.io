---
layout: page
title: How to specify which Java build image for CI
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 11
---

Back-end Java-based modules can specify which build image to use during the Jenkins continuous integration builds.

For projects that use Java 11:

* In Jenkinsfile, add this to the "buildMvn" section: `buildNode = 'jenkins-agent-java11'`
* In Dockerfile, use: `FROM folioci/alpine-jre-openjdk11:latest`
* Additional [upgrade notes](https://github.com/folio-org/raml-module-builder/blob/master/doc/upgrading.md#version-310) for projects based on RAML Module Builder (RMB).

Otherwise the default is currently Java 8:

* In Jenkinsfile, no configuration is needed
* In Dockerfile, use: `FROM folioci/alpine-jre-openjdk8:latest`

As some Java-based projects do not use the "buildMvn" pipeline, they can specify the agent node in their Jenkinsfile:

```
agent {
  node {
    label 'jenkins-agent-java11'
  }
}
```

<div class="folio-spacer-content"></div>

