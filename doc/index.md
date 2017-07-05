---
layout: page
title: Documentation
---

Documentation for the various components of FOLIO is in continuous
development. Since the system is composed of many separate components,
each component is documented individually. The best places to start are
the [FOLIO Developer's Curriculum](http://dev.folio.org/curriculum), which
is a series of self-paced or instructor-guided lessons, and the early chapters
of the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which describe the system as a whole and explain how the parts fit
together.

In the context of those early chapters, you may then wish to go on to:

## Community and contribution

The [community section](../community/) explains how to be involved,
provides the contribution guidelines, lists the various collaboration tools
and has some recommendations about when to use each.

## Developer's curriculum
The [FOLIO Developer's Curriculum](http://dev.folio.org/curriculum) is a series
of lessons that can be followed on your own or can form the basis of an
instructor-led workshop.

## Core code

The most important technical document is the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which after the introductory sections already described, goes into
detail about the Okapi API Gateway that controls a FOLIO system.

## Modules

The [FOLIO-Sample-Modules
guide](https://github.com/folio-org/folio-sample-modules/blob/master/README.md)
contains an explanation of FOLIO modules, a "getting started" guide,
and some sample module code.
[Follow on](https://github.com/folio-org/folio-sample-modules/blob/master/README.md#further-reading)
to the specific documentation for each of those modules.

With that background understanding, see the documentation for each
[server-side](../source-code/#server-side)
module, especially RAML Module Builder (RMB).

## User Interface

The FOLIO user-interface toolkit is called Stripes. It is described in the
[Stripes Core README](https://github.com/folio-org/stripes-core/blob/master/README.md),
which leads to the related documentation.

With that background understanding, see the documentation for each
[client-side](../source-code/#client-side)
module, especially the "ui-users".

The
[okapi-stripes](https://github.com/folio-org/okapi-stripes/blob/master/README.md)
is a special Okapi module used to generate Stripes-based UIs
for individual FOLIO tenants.

## Running a complete system

The document
[Running a complete FOLIO system](https://github.com/folio-org/ui-okapi-console/blob/master/doc/running-a-complete-system.md)
explains ways to enable a development system running the Okapi gateway,
various server-side modules, sample data, and the Stripes UI development server.
It goes on to explain another way to configure modules using the Okapi Console front-end.

Use [folio-ansible](https://github.com/folio-org/folio-ansible/blob/master/README.md)
for a quick-start FOLIO installation as a virtual machine using Vagrant and Ansible.
This also provides various pre-built "black boxes" including
"folio/stable" and "folio/testing".
The current built boxes are also available to download from
[Vagrant Cloud](https://app.vagrantup.com/folio).
The list of module versions for each box is shown in its change-log.

## Guides

<!-- ../../okapi/doc/md2toc -l 2 -h 3 index.md -->
* [Background orientation](#background-orientation)
* [Setup and configuration](#setup-and-configuration)
* [Getting started](#getting-started)
* [Reference documentation](#reference-documentation)
* [Development tips](#development-tips)
* [Tutorials](#tutorials)
* [Development management](#development-management)
* [Community](#community)
* [Other topics](#other-topics)

### Background orientation

- [Which forum](/community/which-forum) to use for communication:
  Issue tracker, Slack chat, Discuss discussion, GitHub pull requests.
  Some guidelines about when to use each, some usage tips, and links to each.
- [Guidelines for Contributing Code](/community/contrib-code) --
  GitHub Flow, feature branches, pull requests, version numbers, coding style,
  tests, etc.
- A [FOLIO glossary](glossary) of some terms and technologies used in FOLIO.
- [Guidelines for FOLIO issue tracker](/community/guide-issues).

### Setup and configuration

- Some tips to assist developers to configure their
  [local workstation setup](setup).
- [Built artifacts](artifacts) -- released and snapshot FOLIO artifacts in various formats.
Configurations for accessing.
- [Source code](/source-code/) -- explanation of each repository.

### Getting started

- [Primer for frontend development](primer-develop-frontend).

### Reference documentation

- [Overiew](reference) of all technical reference documentation.
- <span id="api-reference"/> The set of automatically generated [API documentation](api).

### Development tips

- Conduct [troubleshooting](troubleshooting).

### Tutorials

- The [FOLIO Developer's Curriculum](/curriculum/) is a series
of lessons that can be followed on your own or can form the basis of an
instructor-led workshop.

### Development management

- [Release procedures](release-procedures).
- The [FOLIO project roadmap](https://wiki.folio.org/display/PC/FOLIO+Roadmap).

### Community

- [Community](/community/)
- [Which forum](/community/which-forum) to use for communication.
- [Special Interest Groups](https://wiki.folio.org/display/PC/Special+Interest+Groups) (SIGs).
- [Guidelines for Contributing Code](/community/contrib-code).

### Other topics

- [Best practices for Dockerfiles](best-practices-dockerfiles).
- The FOLIO [build, test, and deployment infrastructure](automation).
- A proposal for [error response formats](https://github.com/folio-org/okapi/blob/master/doc/error-formats-in-folio.md).
- [FOLIO UX](http://ux.folio.org/) -- user experience (UX) driven design and prototypes.
- [FOLIOForums](https://www.openlibraryenvironment.org/archives/category/olfforum) -- upcoming events and recordings of past ones.
