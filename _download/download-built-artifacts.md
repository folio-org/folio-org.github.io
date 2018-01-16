---
layout: download
title: Download Built Artifacts
heading: Download Built Artifacts
permalink: /download/download-built-artifacts/
---

# Built Artifacts

You will find the latest snapshots and released FOLIO artifacts in this section.  The repositories in this section contain the artifacts in various formats.  Browse the examples in this section to get aquainted with FOLIO in various environments.  Download an artifact to take the first steps in understanding how a portion of our system works in your environment.

There are several repositories that contain snapshot and released FOLIO artifacts in various formats.

## Docker Images

At Docker Hub:

* [https://hub.docker.com/u/folioorg/](https://hub.docker.com/u/folioorg/) released versions
* [https://hub.docker.com/r/folioci/](https://hub.docker.com/r/folioci/) snapshot versions

See [Automation/Docker Hub](/guides/system/#docker-hub) for details.

## Maven Artifacts

Example POM configuration:

```xml
  <repositories>
    <repository>
      <id>folio-nexus</id>
      <name>FOLIO Maven repository</name>
      <url>https://repository.folio.org/repository/maven-folio</url>
    </repository>
  </repositories>
```

Browse at
[https://repository.folio.org/#browse/browse/components](https://repository.folio.org/#browse/browse/components)
and see [Automation/Nexus Repository Manager](/guides/system/#nexus-repository-manager)
for details.

## NPM Packages

For Stripes and UI applications.

Example .npmrc configuration:

```
@folio:registry=https://repository.folio.org/repository/npm-folio/
```

Browse at
[https://repository.folio.org/#browse/browse/components](https://repository.folio.org/#browse/browse/components)
and see [Automation/Nexus Repository Manager](/guides/system/#nexus-repository-manager)
for details.

## Debian~Ubuntu API Repository

Currently only Okapi packages for Ubuntu Xenial.

Example APT source configuration:

```
deb https://repository.folio.org/packages/ubuntu xenial/
```

## Vagrant Boxes

At Vagrant Cloud: [https://app.vagrantup.com/folio](https://app.vagrantup.com/folio)

See [further](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) information.