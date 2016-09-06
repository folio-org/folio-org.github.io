---
layout: page
title: Source Code
---

The FOLIO platform consists of both server-side and client-side components, and
will grow to include library services that run on the platform as modules.
Some sample modules are located in
[folio-sample-modules](https://github.com/folio-org/folio-sample-modules).

Several repositories in the [folio-org GitHub
organization](https://github.com/folio-org) host the core project code.
Third-party modules may be hosted elsewhere.

A good starting point for understanding the FOLIO code is
[Okapi](https://github.com/folio-org/okapi) -- specifically the [Okapi Guide and
Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md), which
introduces the concepts and architecture of the FOLIO platform, and includes
installation instructions and examples.  Okapi is the central hub for
applications running on the FOLIO platform and enables access to other modules
in the architecture.

The FOLIO system is made up of the code in several GitHub repositories.
Each repository contains the code for a single well-defined element of the system. These repositories fall into three
categories:

* _server-side elements_ that provide services and the
infrastructure that they run on;
* _client-side elements_ that provide a
framework for using those services from a Web browser;
* and a few that
fall into neither of these categories.

**PLEASE NOTE** that this is a technology preview following the [release early,
release often](https://en.wikipedia.org/wiki/Release_early,_release_often)
philosophy.  **We want your feedback**, in the form of pull requests, [filed
issues](https://issues.folio.org/) and general discussion on the [Slack-based
chat forum](https://folio-project.slack.com/) or the [Discuss web
forum](https://discuss.folio.org).

## Server-side

The key server-side element is Okapi itself: the FOLIO middleware component
that acts as a gateway for access to all modules, handling redundancy,
sessions, etc.  Individual modules are provided in their own repositories, each
named `mod-`_name_: note that these are mostly at the proof-of-concept stage.
Some of these modules are built from specifications in
[RAML](http://raml.org/), the RESTful API Modeling Language: this process is
facilitated by the code in the `raml-module-builder` repository.

* [okapi](https://github.com/folio-org/okapi) --
Okapi API Gateway proxy/discovery/deployment service.

* [raml-module-builder](https://github.com/folio-org/raml-module-builder) --
framework facilitating easy module creation based on RAML files.

* [mod-circulation](https://github.com/folio-org/mod-circulation) --
circulation demo based on the raml-module-builder and a set of RAML and JSON Schemas. Represents some of the necessary circulation functionality against MongoDB.

* [mod-acquisitions](https://github.com/folio-org/mod-acquisitions) --
demo acquisitions module, based on the raml-module-builder framework, exposing acquisition APIs and objects against MongoDB.

* [mod-acquisitions-postgres](https://github.com/folio-org/mod-acquisitions-postgres) --
a second demo acquisitions module, also based on the
raml-module-builder framework and exposing acquisition APIs and
objects, but implemented with an asynchronous Postgres client.

* [mod-configuration](https://github.com/folio-org/mod-configuration) --
demo configuration module based on the raml-module-builder and a set of RAML and JSON Schemas backed by a MongoDB asynchronous implementation.

* [mod-auth](https://github.com/folio-org/mod-auth) --
Prototype of a [JWT](https://jwt.io/)-based
authentication/authorization module. Will be superseded by a more
capable set of modules handling authentication by various methods,
and generalized permissions-handling.

* [mod-metadata](https://github.com/folio-org/mod-metadata) --
Initial work on a FOLIO metadata store and related knowledge base/cataloging concepts.

## Client-side

Since Okapi represents all the FOLIO functionality as well-behaved web
services, UI code can, of course, be written using any toolkit. However,
we will provide Stripes, a toolkit optimized for accessing Okapi-based
services and wrapping UI functionality into convenient modules. We
envisage that most FOLIO UI work will be done in the context of
Stripes.

Note that Stripes is still in the design phase, so although code
exists and can be run, the APIs are likely to change.

* [stripes-experiments](https://github.com/folio-org/stripes-experiments) --
testing ground for prototype modules that may form part of
Stripes. Most importantly, this contains `stripes-core`, which drives
the whole process; and `stripes-connect`, which manages the connection
of UI components to back-end modules.

* [stripes-loader](https://github.com/folio-org/stripes-loader) --
module loader for Webpack, to enable pluggable Redux
applications. This module is responsible for pulling the required UI modules
into a given Stripes UI.

* [okapi-stripes](https://github.com/folio-org/okapi-stripes) --
server-side module for generating UIs based on Stripes.

## Other projects

* [external-api-testing](https://github.com/folio-org/external-api-testing) --
Various tests of Okapi's APIs.

* [folio-sample-modules](https://github.com/folio-org/folio-sample-modules) --
Various sample modules, illustrating ways to structure a module for
use with Okapi (`hello-vertx` and `simple-vertx`) and how to make a
client-side module (`patrons`).

