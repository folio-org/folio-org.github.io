---
layout: page
title: Source-code overview
permalink: /source-code/
menuInclude: yes
menuLink: yes
menuTopTitle: Source
menuTopIndex: 4
menuSubTitle: Source-code overview
menuSubIndex: 1
---

The FOLIO platform consists of both server-side and client-side components, and
will grow to include library services that run on the platform as modules.
Various repositories in the [folio-org GitHub
organization](https://github.com/folio-org) host the core project code.
Third-party modules may be hosted elsewhere.

The [Source-code map](/source-code/map/) enables navigation to details of modules.

A good starting point for understanding the FOLIO code is
[Okapi](https://github.com/folio-org/okapi) -- specifically the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md), which
introduces the concepts and architecture of the FOLIO platform, and includes
installation instructions and examples.  Okapi is the central hub for
applications running on the FOLIO platform and enable access to other modules
in the architecture.

The FOLIO system is made up of the code in several GitHub repositories.
Each repository contains the code for a single well-defined element of the
system. These repositories fall into three categories:

- _server-side elements_ that provide services and the
  infrastructure that they run on;
- _client-side elements_ that provide a
  framework for using those services from a Web browser;
- and some that fall into neither of these categories.

FOLIO follows the [release early,
release often](https://en.wikipedia.org/wiki/Release_early,_release_often)
philosophy.

**We want your feedback** in the form of pull requests and filed issues
(the README of each module has a link to its issue tracker)
and general discussion via the
[collaboration tools](/community).

## Server-side

The key server-side element is [Okapi](map/#okapi) itself: the FOLIO middleware component
that acts as a gateway for access to all modules, handling redundancy,
sessions, etc.

Individual back-end modules are provided in their separate repositories, each
named following the "`mod-`_name_" [convention](/guidelines/naming-conventions/#module-names).
Each back-end module has its own documentation.

Many of these modules are built from specifications in
[RAML](https://raml.org/), the RESTful API Modeling Language: this process is
facilitated by the code in the [raml-module-builder](map/#raml-module-builder) (RMB -- Framework facilitating easy module creation based on RAML files).
Please pay attention that RAML Module Builder is no longer being extended with new functionality and is in maintenance mode only.

Newly created modules utilise API descriptions as OpenAPI Specification ([OAS](/reference/glossary/#oas)).
[FOLIO Spring-Way](/spring-way/#spring-way) with OpenAPI Specification is the preferred way to create new modules in FOLIO.

Refer to the map for all
[Backend infrastructure repos](map/#backend-infrastructure) and
[Backend mod repos](map/#backend-mod) and
[Backend edge repos](map/#backend-edge) and
[Shared RAML repos](map/#raml-shared).

## Client-side

Since Okapi represents all the FOLIO functionality as well-behaved web
services, UI code can, of course, be written using any toolkit. However,
we will provide Stripes, a toolkit optimized for accessing Okapi-based
services and wrapping UI functionality into convenient modules. We
envisage that most FOLIO UI work will be done in the context of
Stripes.

The stripes [documentation](https://github.com/folio-org/stripes/blob/master/README.md) is the starting point.

Individual front-end UI modules are provided in their separate repositories, each
named following the "`ui-`_name_" convention.
Each front-end module has its own documentation.

Refer to the map for all
[Stripes repos](map/#stripes) and
[Frontend ui repos](map/#ui) and
[Frontend ui plugin repos](map/#ui-plugin).

## Platforms

Stripes Platforms are integrated sets of modules based on the dependencies of that platform's front-end modules.

Refer to the map for all
[Stripes platform repos](map/#platform).

## Other projects

Various other FOLIO projects that do not fit the above classifications are listed separately.

Refer to the map for the various [Other repos](map/#other).

<div class="folio-spacer-content"></div>

