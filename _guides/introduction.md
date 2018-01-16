---
layout: guides
title: Introduction
heading: Introduction
permalink: /guides/introduction/
---

# Introduction

Documentation for the various components of FOLIO is in continuous
development. Since the system is composed of many separate components,
each component is documented individually. The best places to start are
the [FOLIO Developer's Curriculum](/tutorials/foliodeveloperscurr/), which
is a series of self-paced or instructor-guided lessons, and the early chapters
of the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which describe the system as a whole and explain how the parts fit
together.

In the context of those early chapters, you may then wish to go on to:

## Community and Contribution

The [community section](/guidelines/communityguidelines/) explains how to be involved,
provides the contribution guidelines, lists the various collaboration tools
and has some recommendations about when to use each.

## Developer's Curriculum

The [FOLIO Developer's Curriculum](/tutorials/foliodeveloperscurr/) is a series
of lessons that can be followed on your own or can form the basis of an
instructor-led workshop.

## Core Code

The most important technical document is the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md),
which after the introductory sections already described, goes into
detail about the Okapi API Gateway that controls a FOLIO system.

### Fundamental documentation

- [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).
- [FOLIO-Sample-Modules guide](https://github.com/folio-org/folio-sample-modules/blob/master/README.md).
- [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework.
- Each [server-side](/source/components/) and [client-side](/source/components/)
module's own documentation.
- [Stripes Core README](https://github.com/folio-org/stripes-core/blob/master/README.md)
guides to all front-end documentation.
- [Stripes entities: packages, modules, apps and more](https://github.com/folio-org/stripes-core/blob/master/doc/modules-apps-etc.md).
- [The Stripes Module Developer's Guide](https://github.com/folio-org/stripes-core/blob/master/doc/dev-guide.md)
for those writing UI modules for Stripes.
- [Regression tests for FOLIO UI](https://github.com/folio-org/ui-testing).
The testing framework is explained. Guidelines for module developers.
- [Permissions in Stripes and FOLIO](https://github.com/folio-org/stripes-core/blob/master/doc/permissions.md).

## Server Side Modules

The [FOLIO-Sample-Modules guide](https://github.com/folio-org/folio-sample-modules/blob/master/README.md)
contains an explanation of FOLIO modules, a "getting started" guide,
and some sample module code.
[Follow on](https://github.com/folio-org/folio-sample-modules/blob/master/README.md#further-reading)
to the specific documentation for each of those modules.

With that background understanding, see the documentation for each
[server-side](/source/components/)
module, especially RAML Module Builder (RMB).

## Client Side Modules

The FOLIO user-interface toolkit is called Stripes. It is described in the
[Stripes Core README](https://github.com/folio-org/stripes-core/blob/master/README.md),
which leads to the related documentation.

With that background understanding, see the documentation for each
[client-side](/source/components/)
module, especially the "ui-users".

The
[okapi-stripes](https://github.com/folio-org/okapi-stripes/blob/master/README.md)
is a special Okapi module used to generate Stripes-based UIs
for individual FOLIO tenants.

