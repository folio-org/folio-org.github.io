---
layout: page
title: General troubleshooting
permalink: /doc/troubleshooting/
menuInclude: no
menuLink: no
menuTopTitle: Documentation
---

A collection of general tips to assist developers to conduct troubleshooting.
Some FOLIO repositories also have specific notes.

<!-- ../../okapi/doc/md2toc -l 2 -h 3 troubleshooting.md -->
* [Other troubleshooting documents](#other-troubleshooting-documents)
* [Keep system tools up-to-date](#keep-system-tools-up-to-date)
* [Update git submodules](#update-git-submodules)
* [Do development and operations as a regular user](#do-development-and-operations-as-a-regular-user)
* [Launching Vagrant on Windows](#launching-vagrant-on-windows)
* [Missing certificate authority for Let's Encrypt](#missing-certificate-authority-for-lets-encrypt)

## Other troubleshooting documents

* [Stripes troubleshooting](https://github.com/folio-org/stripes-core/blob/master/doc/troubleshooting.md)
* [Vagrant boxes troubleshooting](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#troubleshootingknown-issues)

## Keep system tools up-to-date

As [explained](/doc/setup#introduction) in the FOLIO setup documentation,
keeping the operating system and tools up-to-date will generally help to
avoid issues.
See [minimum versions](/doc/setup#tools) of some tools.

## Update git submodules

Some FOLIO repositories utilize “git submodules” for sections of common code.
Some git clients do not handle this properly.
See [notes](/doc/setup#update-git-submodules).

## Do development and operations as a regular user

As usual, do all development and running as a regular user, not as root.
Otherwise there will be strange behaviour, and various facilities and
tools might not be available.
For example, Postgres (including the embedded one) refuses to run as root.

## Launching Vagrant on Windows

If launching Vagrant from a Windows Command Prompt, be sure to use _Run As Administrator..._
when opening the Command Prompt itself (cmd.exe).
If you are seeing the error _"EPROTO: protocol error, symlink"_, the likely cause is that
Vagrant was not launched with administrator privileges.
See issue [STRIPES-344](https://issues.folio.org/browse/STRIPES-344) for details.

## Missing certificate authority for Let's Encrypt

If you are using a version of the Oracle JDK prior to `1.8.0_101`
then the [Let's Encrypt](https://letsencrypt.org/)
certificate authority is not in the Java trust store
([see notes](https://stackoverflow.com/questions/34110426/does-java-support-lets-encrypt-certificate)).
So it will not be possible to download components from the FOLIO Maven
repository. You will see error messages like:

> Could not resolve dependencies for project org.folio:mod-users:jar:0.1-SNAPSHOT: Failed to collect dependencies at org.folio:domain-models-api-interfaces:jar:0.0.1-SNAPSHOT: Failed to read artifact descriptor for org.folio:domain-models-api-interfaces:jar:0.0.1-SNAPSHOT: Could not transfer artifact org.folio:domain-models-api-interfaces:pom:0.0.1-SNAPSHOT from/to folio-nexus (https://repository.folio.org/repository/maven-folio): sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target -> [Help 1]

The fix is just to replace your JDK with a sufficiently recent replacement.
(Or you can use OpenJDK, which has supported Let's Encrypt for longer.)
