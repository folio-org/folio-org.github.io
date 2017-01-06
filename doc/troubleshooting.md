---
layout: page
title: General troubleshooting
---

A collection of general tips to assist developers to conduct troubleshooting.
Some FOLIO repositories also have specific notes.

<!-- ../../okapi/doc/md2toc -l 2 -h 3 troubleshoot.md -->
* [Keep system tools up-to-date](#keep-system-tools-up-to-date)
* [Missing certificate authority for Let's Encrypt](#missing-certificate-authority-for-lets-encrypt)
* [Update git submodules](#update-git-submodules)

## Keep system tools up-to-date

As [explained](setup#up-to-date) in the FOLIO setup documentation,
keeping the operating system and tools up-to-date will generally help to
avoid issues.

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

## Update git submodules

Some FOLIO repositories utilize “git submodules” for sections of common code.
Some git clients do not handle this properly.
See [notes](setup#update-git-submodules).
