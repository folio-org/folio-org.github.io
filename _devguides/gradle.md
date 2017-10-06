---
layout: devguides
title: Gradle-Based Modules
heading: Gradle Based Modules
permalink: /devguides/gradle/
---

The procedure for [Gradle](https://gradle.org/)-based modules (such as [mod-inventory](https://github.com/folio-org/mod-inventory) or [mod-circulation](https://github.com/folio-org/mod-circulation)) is very similar to [maven-based modules](/devguides/maven/).

Follow all of the steps for a maven-based module, except [ensure POM declarations](/devguides/maven/#ensure-pom-declarations) and replacing
[Prepare and perform the source release](/devguides/maven/#prepare-and-perform-the-source-release) with the steps outlined below.

### Change the release version

Using the example of releasing version 4.4.0 of the mod-inventory module for context, the top of the [gradle build configuration](https://github.com/folio-org/mod-inventory/blob/master/build.gradle) will look something similar to:

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
