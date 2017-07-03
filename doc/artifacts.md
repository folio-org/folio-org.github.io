---
layout: page
title: Built artifacts
---

There are several repositories that contain snapshot and released FOLIO artifacts in various formats.

<!-- ../../okapi/doc/md2toc -l 2 -h 3 artifacts.md -->

## Docker images

At Docker Hub: [https://hub.docker.com/u/folioorg/](https://hub.docker.com/u/folioorg/)

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

## NPM packages

For Stripes and UI applications.

Example .npmrc configuration:

```
@folio:registry=https://repository.folio.org/repository/npm-folio/
```

## Debian/Ubuntu APT repository

Currently only Okapi packages for Ubuntu Xenial.

Example APT source configuration:

```
deb https://repository.folio.org/packages/ubuntu xenial/
```
