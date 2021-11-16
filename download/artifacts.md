---
layout: page
title: Built artifacts
permalink: /download/artifacts/
menuInclude: yes
menuLink: yes
menuTopTitle: Download
menuSubs:
- title: Download introduction
  url: /download/
  index: 1
- title: Built artifacts
  index: 2
---

There are several repositories that contain snapshot and released FOLIO artifacts in various formats.

## Docker images

At Docker Hub:

* [https://hub.docker.com/u/folioorg/](https://hub.docker.com/u/folioorg/) released versions
* [https://hub.docker.com/u/folioci/](https://hub.docker.com/u/folioci/) snapshot versions

See [Automation/Docker Hub](/guides/automation#docker-hub) for details.

Docker images are the primary distribution model for FOLIO modules.

To run the images you will need the Docker Engine or Docker Desktop runtime.
Or use them via a FOLIO prebuilt Vagrant [box](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) VM.

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
[https://repository.folio.org/#browse/browse](https://repository.folio.org/#browse/browse)
and see [Automation/Nexus Repository Manager](/guides/automation#nexus-repository-manager)
for details.

## NPM packages

For Stripes and UI applications.

Example .npmrc configuration:

```
@folio:registry=https://repository.folio.org/repository/npm-folio/
```

Browse at
[https://repository.folio.org/#browse/browse](https://repository.folio.org/#browse/browse)
and see [Automation/Nexus Repository Manager](/guides/automation#nexus-repository-manager)
for details.

## Debian/Ubuntu APT repository

Okapi packages before version 4 are available for Ubuntu Xenial.

Example APT source configuration:

```
deb https://repository.folio.org/packages/ubuntu xenial/
```

Okapi version 4 and later are available for Ubuntu Focal Fossa:


```
deb https://repository.folio.org/packages/ubuntu focal/
```

## Vagrant boxes

At Vagrant Cloud: [https://app.vagrantup.com/folio](https://app.vagrantup.com/folio)

See [further](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md) information.

<div class="folio-spacer-content"></div>

