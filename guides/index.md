---
layout: page
title: Guides
permalink: /guides/
menuInclude: yes
menuLink: yes
menuTopTitle: Guides
menuTopIndex: 5
menuSubTitle: Guides overview
menuSubIndex: 1
menuSubs:
- title: Guides
  anchorId: guides
- title: FAQs
  url: /faqs/
---

Documentation for the various components of FOLIO is in continuous
development. Since the system is composed of many separate components,
each component is documented individually. The best places to start are
the [FOLIO Developer's Curriculum](/tutorials/curriculum/), which
is a series of self-paced or instructor-guided lessons, and the early chapters
of the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which describe the system as a whole and explain how the parts fit
together.

In the context of those early chapters, you may then wish to go on to:

## Community and contribution

The [community section](/community/) explains how to be involved,
provides the contribution guidelines, lists the various collaboration tools
and has some recommendations about when to use each.

## Developer's curriculum
The [FOLIO Developer's Curriculum](/tutorials/curriculum/) is a series
of lessons that can be followed on your own or can form the basis of an
instructor-led workshop.

## Core code

The most important technical document is the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which after the introductory sections already described, goes into
detail about the Okapi API Gateway that controls a FOLIO system.

## Modules

The [FOLIO-Sample-Modules guide](https://github.com/folio-org/folio-sample-modules/blob/master/README.md)
contains an explanation of FOLIO modules, a "getting started" guide,
and some sample module code.
[Follow on](https://github.com/folio-org/folio-sample-modules/blob/master/README.md#further-reading)
to the specific documentation for each of those modules.

With that background understanding, see the documentation for each
[server-side](/source-code/#server-side)
module, especially RAML Module Builder (RMB).

## User Interface

The FOLIO user-interface toolkit is called Stripes. It is described in the
[Stripes Core README](https://github.com/folio-org/stripes-core/blob/master/README.md),
which leads to the related documentation.

With that background understanding, see the documentation for each
[client-side](/source-code/#client-side)
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
* [Fundamental documentation](#fundamental-documentation)
* [Development tips](#development-tips)
* [Tutorials](#tutorials)
* [Development management](#development-management)
* [Community](#community)
* [Other topics](#other-topics)

### Background orientation

- [Which forum](/guidelines/which-forum/) to use for communication:
  Issue tracker, Slack chat, Discuss discussion, GitHub pull requests.
  Some guidelines about when to use each, and some usage tips.
  The [concise list](/community/#collaboration-tools) of forums.
- [Guidelines for Contributing Code](/community/contrib-code) --
  GitHub Flow, feature branches, pull requests, version numbers, coding style,
  tests, etc.
- [FOLIO Project Contributor License Agreement](/community/cla-process).
- A [FOLIO glossary](/reference/glossary) of some terms and technologies used in FOLIO.
- [Guidelines for FOLIO issue tracker](/guidelines/issue-tracker/).
- [Search dev.folio.org](/search) and [other search and report facilities](/search-other).

### Setup and configuration

- Some tips to assist developers to configure their
  [local workstation setup](setup).
- [Built artifacts](/download/artifacts/) -- released and snapshot FOLIO artifacts in various formats.
Configurations for accessing.
- [Source code](/source-code/) -- explanation of each repository.

### Getting started

- [FOLIO uses any programming language](any-programming-language/).
- [Primer for back-end development](/start/primer-develop-backend/).
- [Primer for front-end development](/start/primer-develop-frontend/).

### Reference documentation

- [Overiew](/reference/) of all technical reference documentation.
- <span id="api-reference"/> The set of automatically generated [API documentation](/reference/api/).

### Fundamental documentation

- [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).
- [FOLIO-Sample-Modules guide](https://github.com/folio-org/folio-sample-modules/blob/master/README.md).
- [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework.
- Each [server-side](/source-code/#server-side) and [client-side](/source-code/#client-side)
module's own documentation.
- [Stripes Core README](https://github.com/folio-org/stripes-core/blob/master/README.md)
guides to all front-end documentation.
- [Stripes entities: packages, modules, apps and more](https://github.com/folio-org/stripes-core/blob/master/doc/modules-apps-etc.md).
- [The Stripes Module Developer's Guide](https://github.com/folio-org/stripes-core/blob/master/doc/dev-guide.md)
for those writing UI modules for Stripes.
- [Regression tests for FOLIO UI](https://github.com/folio-org/ui-testing).
The testing framework is explained. Guidelines for module developers.
- [Permissions in Stripes and FOLIO](https://github.com/folio-org/stripes-core/blob/master/doc/permissions.md).

### Development tips

- Conduct [troubleshooting](troubleshooting).
- [Code analysis and linting facilities](code-analysis) explains ESLint, SonarQube, other lint tools, and preparing for pull requests.
- For Contextual Query Language (CQL) examples, see the [Glossary](/reference/glossary/#cql), the FOLIO [CQL to PostgreSQL JSON converter](https://github.com/folio-org/cql2pgjson-java), the [API docs](/reference/api/), and the debug output for tests in each backend module.
- Use [raml-cop](/guides/raml-cop/) to assess RAMLs, schema, and examples. A guide to its use with some explanations of its messages.

### Tutorials

- The [FOLIO Developer's Curriculum](/tutorials/curriculum/) is a series
of lessons that can be followed on your own or can form the basis of an
instructor-led workshop.

### Development management

- [Release procedures](/guidelines/release-procedures/).
- [Search and report facilities](/search-other) (e.g. open pull requests needing review).
- [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/).
- The [FOLIO Project Roadmap](https://wiki.folio.org/display/PC/FOLIO+Roadmap) including the development and milestone plan for Version 1 and the feature backlog,
and the [FOLIO Development Process Overview](https://wiki.folio.org/display/COMMUNITY/FOLIO+Development+Process+Overview), and other important documents and resources are listed at the [Wiki](https://wiki.folio.org).

### Community

- [Community](/community/)
- [Which forum](/guidelines/which-forum/) to use for communication.
- [Special Interest Groups](https://wiki.folio.org/display/PC/Special+Interest+Groups) (SIGs).
- [Guidelines for Contributing Code](/community/contrib-code).

### Other topics

- [Best practices for Dockerfiles](best-practices-dockerfiles).
- The FOLIO [build, test, and deployment infrastructure](automation).
- A proposal for [error response formats](https://github.com/folio-org/okapi/blob/master/doc/error-formats-in-folio.md).
- [FOLIO UX](http://ux.folio.org/) -- user experience (UX) driven design and prototypes.
- [Events and presentations](events).
