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
[Okapi](https://github.com/folio-org/okapi) -- specifically the
[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md), which
introduces the concepts and architecture of the FOLIO platform, and includes
installation instructions and examples.  Okapi is the central hub for
applications running on the FOLIO platform and enables access to other modules
in the architecture.

The FOLIO system is made up of the code in several GitHub repositories.
Each repository contains the code for a single well-defined element of the
system. These repositories fall into three categories:

- _server-side elements_ that provide services and the
  infrastructure that they run on;
- _client-side elements_ that provide a
  framework for using those services from a Web browser;
- and a few that fall into neither of these categories.

**PLEASE NOTE** that this is a technology preview following the [release early,
release often](https://en.wikipedia.org/wiki/Release_early,_release_often)
philosophy.  **We want your feedback** in the form of pull requests and filed
issues and general discussion via the
[collaboration tools](../community).

## Server-side

The key server-side element is Okapi itself: the FOLIO middleware component
that acts as a gateway for access to all modules, handling redundancy,
sessions, etc.  Individual modules are provided in their own repositories, each
named `mod-`_name_ (note that these are mostly at the proof-of-concept stage).
Each module has its own documentation.

Some of these modules are built from specifications in
[RAML](http://raml.org/), the RESTful API Modeling Language: this process is
facilitated by the code in the `raml-module-builder` repository.

- [okapi](https://github.com/folio-org/okapi)
  -- Okapi API Gateway proxy/discovery/deployment service.

- [raml](https://github.com/folio-org/raml)
  -- Repository of RAML files, including JSON Schemas, traits and
  resource types centralized for re-usability.
  The [API reference](../doc/#api-reference) documentation is also
  generated.
  This repository is the master location for the traits and resource
  types, while each module is the master for its own schemas, examples,
  and actual RAML files.
  It is included in other repositories via a git sub-module, usually called `raml-util`.

- [raml-module-builder](https://github.com/folio-org/raml-module-builder)
  -- Framework facilitating easy module creation based on RAML files.

- [mod-authtoken](https://github.com/folio-org/mod-authtoken)
  -- Filtering requests based on JWT tokens.

- [mod-login](https://github.com/folio-org/mod-login)
  -- Handles username/password login.

- [mod-permissions](https://github.com/folio-org/mod-permissions)
  -- Handles permissions and permissions/user associations.

- [mod-users](https://github.com/folio-org/mod-users)
  -- Provides user management.

- [mod-users-bl](https://github.com/folio-org/mod-users-bl)
  -- Business logic "join" module to provide simple access to all
  user-centric data.

- [mod-inventory](https://github.com/folio-org/mod-inventory)
  -- Provides basic physical item inventory management.

- [mod-inventory-storage](https://github.com/folio-org/mod-inventory-storage)
  -- Persistent storage to complement the inventory module.

- [mod-circulation](https://github.com/folio-org/mod-circulation)
  -- Circulation capabilities, including loan items from the inventory.

- [mod-circulation-storage](https://github.com/folio-org/mod-circulation-storage)
  -- Persistent storage to complement the circulation module.

- [mod-configuration](https://github.com/folio-org/mod-configuration)
  -- Demo configuration module based on the raml-module-builder and a set
  of RAML and JSON Schemas backed by a PostgreSQL asynchronous implementation.

- [mod-notes](https://github.com/folio-org/mod-notes)
  -- Notes on all types of objects.

- [mod-acquisitions](https://github.com/folio-org/mod-acquisitions)
  -- Demo acquisitions module, based on the raml-module-builder framework,
  exposing acquisition APIs and objects against MongoDB.

- [mod-acquisitions-postgres](https://github.com/folio-org/mod-acquisitions-postgres)
  -- A second demo acquisitions module, also based on the
  raml-module-builder framework and exposing acquisition APIs and
  objects, but implemented with an asynchronous Postgres client.

## Client-side

Since Okapi represents all the FOLIO functionality as well-behaved web
services, UI code can, of course, be written using any toolkit. However,
we will provide Stripes, a toolkit optimized for accessing Okapi-based
services and wrapping UI functionality into convenient modules. We
envisage that most FOLIO UI work will be done in the context of
Stripes.

The stripes-core [documentation roadmap](https://github.com/folio-org/stripes-core#documentation-roadmap) is the starting point.
Each module has its own documentation.

Note that Stripes is still in the design phase, so although code
exists and can be run, the APIs are likely to change.

- [stripes-core](https://github.com/folio-org/stripes-core)
  -- The UI framework.
  Includes extensive documentation.

- [stripes-sample-platform](https://github.com/folio-org/stripes-sample-platform)
  -- Configuration for a sample platform and to run a local
  Stripes UI development server.

- [stripes-components](https://github.com/folio-org/stripes-components)
  -- A component library for Stripes.
  Includes documentation for each library, and guides to assist their development.

- [stripes-connect](https://github.com/folio-org/stripes-connect)
  -- Manages the connection of UI components to back-end modules.

- [stripes-form](https://github.com/folio-org/stripes-form)
  -- A redux-form wrapper for Stripes.

- [stripes-logger](https://github.com/folio-org/stripes-logger)
  -- Simple category-based logging for Stripes.

- [ui-users](https://github.com/folio-org/ui-users)
  -- Stripes UI module: administrating users.

- [ui-items](https://github.com/folio-org/ui-items)
  -- Stripes UI module: administrating bibliographic items.

- [ui-requests](https://github.com/folio-org/ui-requests)
  -- Stripes UI module: making requests on items.

- [ui-checkin](https://github.com/folio-org/ui-checkin)
  -- Stripes UI module: checking in items with simulated scans.

- [ui-checkout](https://github.com/folio-org/ui-checkout)
  -- Stripes UI module: checking out items with simulated scans.

- [ui-organization](https://github.com/folio-org/ui-organization)
  -- Stripes UI module: managing organization settings.

- [ui-developer](https://github.com/folio-org/ui-developer)
  -- Stripes UI module: developer facilities,
  e.g. managing local developer settings.

- [ui-plugin-find-user](https://github.com/folio-org/ui-plugin-find-user)
  -- Stripes UI plugin: User-finder.

- [stripes-loader](https://github.com/folio-org/stripes-loader)
  -- Module loader for Webpack, to enable pluggable Redux applications.
  This module is responsible for pulling the required UI modules
  into a given Stripes UI.

- [okapi-stripes](https://github.com/folio-org/okapi-stripes)
  -- Server-side module for generating UIs based on Stripes.

- [stripes-demo-platform](https://github.com/folio-org/stripes-demo-platform)
  -- Stripes platform for building the demo site.

- [ui-okapi-console](https://github.com/folio-org/ui-okapi-console)
  -- Stripes UI module: console for administrating Okapi.

- [stripes-experiments](https://github.com/folio-org/stripes-experiments)
  -- Testing ground for prototype modules that may form part of
  Stripes.

## Other projects

- [folio-sample-modules](https://github.com/folio-org/folio-sample-modules)
  -- Various sample modules, illustrating ways to structure a module for
  use with Okapi (e.g. `hello-vertx` and `simple-vertx` and `simple-perl`).

- [folio-ansible](https://github.com/folio-org/folio-ansible)
  -- Sample Ansible playbook and roles for FOLIO (and Vagrant).
  Get a FOLIO installation up and running quickly.
  Read the docs there, and follow to build the boxes.
  The current built boxes are also available to download from
  [Vagrant Cloud](https://app.vagrantup.com/folio).

- [cql2pgjson-java](https://github.com/folio-org/cql2pgjson-java)
  -- CQL (Contextual Query Language) to PostgreSQL JSON converter in Java.

- [ui-testing](https://github.com/folio-org/ui-testing)
  -- Regression tests for FOLIO UI.

- [folio-org.github.io](https://github.com/folio-org/folio-org.github.io)
  -- The source for this dev.folio.org website.
