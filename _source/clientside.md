---
layout: source
title: Client Side Components
heading: Client Side Components
permalink: /source/clientside/
---

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

- [stripes-redux](https://github.com/folio-org/stripes-redux)
  -- A collection of utility functions and middleware for redux and redux-observable.

- [stripes-util-notes](https://github.com/folio-org/stripes-util-notes)
  -- A utility module for attaching notes to entities such as users and items.
  
- [stripes-logger](https://github.com/folio-org/stripes-logger)
  -- Simple category-based logging for Stripes.

- [ui-users](https://github.com/folio-org/ui-users)
  -- Stripes UI module: administrating users.
  
- [ui-instances](https://github.com/folio-org/ui-instances)
  -- Stripes UI module: administrating instances.

- [ui-items](https://github.com/folio-org/ui-items)
  -- Stripes UI module: administrating bibliographic items.

- [ui-requests](https://github.com/folio-org/ui-requests)
  -- Stripes UI module: making requests on items.

- [ui-checkin](https://github.com/folio-org/ui-checkin)
  -- Stripes UI module: checking in items with simulated scans.

- [ui-checkout](https://github.com/folio-org/ui-checkout)
  -- Stripes UI module: checking out items with simulated scans.
  
- [ui-circulation](https://github.com/folio-org/ui-circulation)
  -- Stripes UI module: Circulation.

- [ui-organization](https://github.com/folio-org/ui-organization)
  -- Stripes UI module: managing organization settings.
  
- [ui-plugin-find-user](https://github.com/folio-org/ui-plugin-find-user)
  -- Stripes UI plugin: User-finder.

- [ui-developer](https://github.com/folio-org/ui-developer)
  -- Stripes UI module: developer facilities,
  e.g. managing local developer settings.

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
  The testing framework is explained. Guidelines for module developers.

- [folio-org.github.io](https://github.com/folio-org/folio-org.github.io)
  -- The source for this dev.folio.org website.
