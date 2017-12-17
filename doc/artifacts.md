---
layout: page
title: Built artifacts
permalink: /doc/artifacts/
menuInclude: yes
menuLink: yes
menuTopTitle: Download
menuTopIndex: 4
menuSubTitle: Overview
menuSubIndex: 1
menuSubs:
- title: Docker images
  anchorId: docker-images
- title: Maven artifacts
  anchorId: maven-artifacts
- title: NPM packages
  anchorId: npm-packages
- title: APT repository
  anchorId: debianubuntu-apt-repository
- title: Vagrant boxes
  anchorId: vagrant-boxes
---

There are several repositories that contain snapshot and released FOLIO artifacts in various formats.

## Docker images

At Docker Hub:

* [https://hub.docker.com/u/folioorg/](https://hub.docker.com/u/folioorg/) released versions
* [https://hub.docker.com/r/folioci/](https://hub.docker.com/r/folioci/) snapshot versions

See [Automation/Docker Hub](/doc/automation#docker-hub) for details.

## Maven artifacts

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
and see [Automation/Nexus Repository Manager](/doc/automation#nexus-repository-manager)
for details.

## NPM packages

For Stripes and UI applications.

Example .npmrc configuration:

```
@folio:registry=https://repository.folio.org/repository/npm-folio/
```

Browse at
[https://repository.folio.org/#browse/browse/components](https://repository.folio.org/#browse/browse/components)
and see [Automation/Nexus Repository Manager](/doc/automation#nexus-repository-manager)
for details.

## Debian/Ubuntu APT repository

Currently only Okapi packages for Ubuntu Xenial.

Example APT source configuration:

```
deb https://repository.folio.org/packages/ubuntu xenial/
```

## Vagrant boxes

At Vagrant Cloud: [https://app.vagrantup.com/folio](https://app.vagrantup.com/folio)

See [further](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) information.

