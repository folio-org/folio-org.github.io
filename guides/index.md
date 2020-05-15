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
the early chapters
of the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which describe the system as a whole and explain how the parts fit
together.

In the context of those early chapters, you may then wish to go on to:

## Community and contribution

The [community section](/community/) explains how to be involved,
provides the contribution guidelines, lists the various collaboration tools
and has some recommendations about when to use each.

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
[Stripes README](https://github.com/folio-org/stripes/blob/master/README.md),
which leads to the related documentation.

With that background understanding, see the documentation for each
[client-side](/source-code/#client-side)
module, especially the "ui-users".

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
* [Development operations](#development-operations)
* [Community](#community)
* [Other topics](#other-topics)

### Background orientation

Refer to the [Guidelines](/guidelines/#background-orientation) section.

Other orientation guides:

- [Navigation of commits and CI via GitHub and Jenkins](navigate-commits/).
- [Search dev.folio.org](/search) and [other search and report facilities](/search-other).

### Setup and configuration

- Some tips to assist developers to configure their
  [local workstation setup](developer-setup).
- [Built artifacts](/download/artifacts/) -- released and snapshot FOLIO artifacts in various formats.
Configurations for accessing.
- [Source code](/source-code/) -- explanation of each repository.

### Getting started

Refer to the [Start](/start/) section.

- [Overview](/start/overview/) high-level summary of "getting started" points for a new developer -- an on-boarding guide.
- Having followed that getting started documentation and understanding the fundamentatal documentation, then follow [Running a local FOLIO system](/guides/run-local-folio/).
- The [Commence a module - structure and configuration](/guides/commence-a-module/) guide explains a consistent layout for back-end and front-end modules.

### Reference documentation

- [Overiew](/reference/) of all technical reference documentation.
- <span id="api-reference"/> The set of automatically generated [API documentation](/reference/api/).

### Fundamental documentation

These are listed in the [Start](/start/) section.

### Development tips

- [Manage notifications to keep abreast](manage-notifications/).
- Conduct [troubleshooting](troubleshooting).
- [Code analysis and linting facilities](code-analysis) explains ESLint, SonarQube, other lint tools, and preparing for pull requests.
- [Branch preview on Kubernetes infrastructure](branch-preview-kubernetes/).
- [Branch preview mode for UI modules](branch-preview/).
- For Contextual Query Language (CQL) examples, see the [Glossary](/reference/glossary/#cql), the FOLIO [CQL to PostgreSQL JSON converter](https://github.com/folio-org/raml-module-builder#cql-contextual-query-language), the [API docs](/reference/api/), and the debug output for tests in each backend module.
- Use [raml-cop](raml-cop/) to assess RAMLs, schema, and examples. A guide to its use with some explanations of its messages.
- [Conduct API testing](api-testing/) using Postman collections and Newman against a running module.
- [Describe schema and properties](describe-schema/).
- Explain [ModuleDescriptors](module-descriptor/) and default [LaunchDescriptors](module-descriptor/#launchdescriptor-properties).
- [Conduct cross-module joins via their APIs](cross-module-joins).
- [Working with dates and times](dates-and-times/).
- [How to check for a valid UUID](uuids).
- [User experience design](user-experience-design/).
- [Accessible Routing in FOLIO](https://github.com/folio-org/stripes-components/blob/master/docs/patterns/AccessibleRouting.md) explains assisted navigation.
- [FOLIO App Information, Tips, and Tricks](https://wiki.folio.org/display/FOLIOtips/).
  Provides overview information for each individual app.
  Includes [Settings](https://wiki.folio.org/display/FOLIOtips/Settings) documentation for each individual app.
- [Performance optimization](performance-optimization/).

### Tutorials

- [Using a FOLIO virtual machine](/tutorials/folio-vm/) -- Explains how to utilise a FOLIO virtual machine (VM).

### Development management

- [Release procedures](/guidelines/release-procedures/).
- [Regular FOLIO releases](regular-releases/).
- [Search and report facilities](/search-other) (e.g. open pull requests needing review).
- [Technical Designs and Decisions](https://wiki.folio.org/display/DD/). Wiki space to document feature-level designs and decisions.
- [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/)
and when ready [install](/faqs/how-to-install-new-module/) it to platform and reference environments for snapshot and testing builds.
- [Rename a module](rename-module/).
- [Maintain tidy repositories](tidy-repository/).
- <a id="roadmap"></a>The [overview](https://www.folio.org/platform/) and the [FOLIO Project Roadmap](https://wiki.folio.org/display/PC/FOLIO+Roadmap) including the development and milestone plan for Version 1 and the feature backlog,
and the [FOLIO Development Process Overview](https://wiki.folio.org/display/COMMUNITY/FOLIO+Development+Process+Overview), and other important documents and resources are listed at the [Wiki](https://wiki.folio.org).

### Development operations

For people assisting with the FOLIO development operations infrastructure (DevOps) there are various notes.
For example regarding operation, enhancement, and configuration of Jenkins continuous integration.

- [DevOps introduction](devops-introduction/).
- [DevOps - Verify task acceptance criteria](devops-verify-task-acceptance/).
- [DevOps - Install a new back-end module to reference environments](devops-install-backend-module/).

### Community

- [Community](/community/)
- [Which forum](/guidelines/which-forum/) to use for communication.
- [Special Interest Groups](https://wiki.folio.org/display/PC/Special+Interest+Groups) (SIGs).
- [Guidelines for Contributing Code](/guidelines/contributing/).

### Other topics

- [Best practices for Dockerfiles](best-practices-dockerfiles).
- The FOLIO [build, test, and deployment infrastructure](automation/).
- A proposal for [error response formats](https://github.com/folio-org/okapi/blob/master/doc/error-formats-in-folio.md).
- [Events and presentations](/community/events/).

## FAQs

- [Frequently asked questions](/faqs/).

Brief explanations of various topics.

