---
layout: source
title: Components
heading: Components
permalink: /source/components/
---

# Components

## Introduction

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
[collaboration tools](/guidelines/communityguidelines/#community-tools).

## Any Programming Language

The design of FOLIO architecture
([microservices](/reference/refinfo/#folio-technologies-and-concepts) and [REST](/reference/refinfo/#folio-technologies-and-concepts))
enables any module to be written in a programming language that the developer is comfortable with. So various programming languages and build environments can be utilized.

### Server-side

The [back-end](/source/components/#server-side-1) modules can utilize any language.
The [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework, is a special module that abstracts much functionality and enables the developer to focus on implementing business functions. Define the APIs and objects in RAML files and schema files, then the RMB generates code and provides tools to help implement the module.
Note that at this stage of the FOLIO project, only this Java-based framework is available.
Other frameworks would be possible.

* Be able to handle the REST interactions according to the [API](/reference/refinfo/#api-specifications) and implement the lifecycle endpoints.
* As [explained](https://github.com/folio-org/okapi/blob/master/doc/guide.md#chunked) in the Okapi Guide, Okapi uses HTTP 1.1 with chunked encoding to make the connections to the modules.

### Client-side

The [front-end](/source/components/#client-side-1) user interface code can be written using any toolkit and programming language, since Okapi represents all of the FOLIO functionality as well-behaved web services.
FOLIO provides the [Stripes](/source/components/#client-side-1) UI toolkit (JavaScript), optimized for accessing Okapi-based services and wrapping UI functionality into convenient modules.
Other toolkits would be possible.

* Be able to handle the REST interactions according to the [API](/reference/refinfo/#api-specifications).
* Be able to manage state and send special headers such as X-Okapi-Tenant.

### Current situation

So far we have concentrated on server-side modules in Java using Vert.x, and
client-side in Node.js and React. Because we use them internally, those technologies will have
a prominent place in the FOLIO ecosystem and, initially, it may be easiest
to get started using them. We provide libraries and utilities that
help with development (especially with writing standard boiler-plate code and
scaffolding) but we hope to eventually gain a wide coverage among other
tools and technologies (e.g. Python, Ruby, etc.). We are counting on an active
engagement from the community to help out in this area.

## Create New Repository

These are notes to assist developers with creating a new FOLIO module as a repository.
Initial setup files and configuration.

Take care to choose wisely for the repository name. It is disruptive to change that.

The following first few items can only be done by the initial creator of the repository or its owners, and should happen early. Use its "Settings" area.

Ensure that access is configured for the relevant FOLIO GitHub [Teams](https://github.com/orgs/folio-org/teams) (e.g. foliodev-core, stripes).

Disable the Issues and Wiki via Settings. We use the FOLIO resources.

Add a concise description to the GitHub repository. Consider that this will also be used elsewhere.

Copy initial files from an existing FOLIO module repository (e.g.
[mod-notes](https://github.com/folio-org/mod-notes),
[stripes-smart-components](https://github.com/folio-org/stripes-smart-components)).
The Stripes/UI/backend modules might be slightly different (e.g. CHANGELOG.md = NEWS.md).

Add LICENSE and CONTRIBUTING.md and README.md files.

Ensure that the copyright and license statement is near the top of the README.
Use the initial year of creation for the date.

Ensure that any package.json and pom.xml etc. type of configuration file has the appropriate "licence" elements.

Add [.editorconfig](/tools/setupdevenv/#coding-style) file.

Add initial NEWS.md or CHANGELOG.md file.

If necessary, add a basic .gitignore file.
Developers will have [their own ~/.gitignore_global](/tools/setupdevenv/#use-gitignore) to handle most.

Add other configuration files. Follow similar existing repositories.
For back-end modules: descriptors/ModuleDescriptor-template.json, Dockerfile, etc.
For front-end modules: package.json, .eslintrc, etc.

Open a Jira issue, so that the project is integrated into Jenkins, the correct permissions are set on the repo, and an appropriate Jira project can be created (if applicable). Add the label 'ci'.

## Server Side

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
  The [API reference](/doc/#api-reference) documentation is also
  generated.
  This repository is the master location for the traits and resource
  types, while each module is the master for its own schemas, examples,
  and actual RAML files.
  It is included in other repositories via a git sub-module, usually called `raml-util`.

- [raml-module-builder](https://github.com/folio-org/raml-module-builder)
  -- Framework facilitating easy module creation based on RAML files.

- [mod-configuration](https://github.com/folio-org/mod-configuration)
  -- Configuration module based on the raml-module-builder and a set
  of RAML and JSON Schemas backed by a PostgreSQL asynchronous implementation.

- [mod-authtoken](https://github.com/folio-org/mod-authtoken)
  -- Filtering requests based on JWT tokens.

- [mod-login](https://github.com/folio-org/mod-login)
  -- Handles username/password login.

- [mod-login-saml](https://github.com/folio-org/mod-login-saml)
  -- Handles SAML login.

- [mod-permissions](https://github.com/folio-org/mod-permissions)
  -- Handles permissions and permissions/user associations.

- [mod-users](https://github.com/folio-org/mod-users)
  -- Provides user management.

- [mod-users-bl](https://github.com/folio-org/mod-users-bl)
  -- Business logic "join" module to provide simple access to all
  user-centric data.

- [mod-user-import](https://github.com/folio-org/mod-user-import)
  -- Importing new or already existing users into FOLIO.

- [mod-inventory](https://github.com/folio-org/mod-inventory)
  -- Provides basic physical item inventory management.

- [mod-inventory-storage](https://github.com/folio-org/mod-inventory-storage)
  -- Persistent storage to complement the inventory module.

- [mod-circulation](https://github.com/folio-org/mod-circulation)
  -- Circulation capabilities, including loan items from the inventory.

- [mod-circulation-storage](https://github.com/folio-org/mod-circulation-storage)
  -- Persistent storage to complement the circulation module.

- [mod-finance](https://github.com/folio-org/mod-finance)
  -- Persistent storage of finance-related data (i.e. funds, ledgers, transactions, etc.)

- [mod-graphql](https://github.com/folio-org/mod-graphql)
  -- Executing GraphQL queries.
  
- [mod-kb-ebsco](https://github.com/folio-org/mod-kb-ebsco)
  -- Broker communication with the EBSCO knowledge base.  

- [mod-notes](https://github.com/folio-org/mod-notes)
  -- Notes on all types of objects.

- [mod-notify](https://github.com/folio-org/mod-notify)
  -- Notifications to the users.

- [mod-codex-mux](https://github.com/folio-org/mod-codex-mux)
  -- Codex Multiplexer.

- [mod-codex-mock](https://github.com/folio-org/mod-codex-mock)
  -- Codex mock module - for testing and development.

- [mod-codex-ekb](https://github.com/folio-org/mod-codex-ekb)
  -- Codex wrapper for the EBSCO knowledge base.

- [mod-codex-inventory](https://github.com/folio-org/mod-codex-inventory)
  -- Codex wrapper for local inventory.

- [mod-cataloging](https://github.com/atcult/mod-cataloging)
  -- FOLIO metadata management / cataloging module.

- [mod-orders](https://github.com/folio-org/mod-orders)
  -- Persistent storage of order data.

- [mod-vendors](https://github.com/folio-org/mod-vendors)
  -- Persistent storage of vendor data.

- [inventory-sample-data](https://github.com/folio-org/inventory-sample-data)
  -- Provides scripts for data preparation and deployment, e.g. MARC.

## Client Side

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

- [stripes-smart-components](https://github.com/folio-org/stripes-smart-components)
  -- A suite of smart components. Each communicates with an Okapi web-service in order to provide the facilities that it renders.

- [stripes-connect](https://github.com/folio-org/stripes-connect)
  -- Manages the connection of UI components to back-end modules.

- [stripes-form](https://github.com/folio-org/stripes-form)
  -- A redux-form wrapper for Stripes.

- [stripes-logger](https://github.com/folio-org/stripes-logger)
  -- Simple category-based logging for Stripes.

- [stripes-cli](https://github.com/folio-org/stripes-cli)
  -- Command-line interface for creating, building, and testing Stripes UI modules.

- [ui-users](https://github.com/folio-org/ui-users)
  -- Stripes UI module: administrating users.

- [ui-inventory](https://github.com/folio-org/ui-inventory)
  -- Stripes UI module: administrating locally created instances, holdings records and items.

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
  
- [ui-eholdings](https://github.com/folio-org/ui-eholdings)
  -- Stripes UI module: E-holdings. 

- [ui-search](https://github.com/folio-org/ui-search)
  -- Stripes UI module: searching, sorting, filtering and viewing records from the FOLIO Codex, an aggregation of bibliographic metadata from multiple sources.

- [ui-organization](https://github.com/folio-org/ui-organization)
  -- Stripes UI module: managing organization settings.

- [ui-plugin-find-user](https://github.com/folio-org/ui-plugin-find-user)
  -- Stripes UI plugin: User-finder.

- [ui-trivial](https://github.com/folio-org/ui-trivial)
  -- Stripes UI module: example application.

- [ui-developer](https://github.com/folio-org/ui-developer)
  -- Stripes UI module: developer facilities,
  e.g. managing local developer settings.

- [eslint-config-stripes](https://github.com/folio-org/eslint-config-stripes)
  -- The shared eslint configuration for stripes applications and extensions.

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

- [ui-testing](https://github.com/folio-org/ui-testing)
  -- Regression tests for FOLIO UI.
  The testing framework is explained. Guidelines for module developers.

- [folio-tools](https://github.com/folio-org/folio-tools)
  -- Various tools and support glue for FOLIO CI.

- [okapi.rb](https://github.com/thefrontside/okapi.rb)
  -- Ruby client to communicate with an OKAPI cluster. Also known as "okapi-cli".

- [curriculum](https://github.com/folio-org/curriculum)
  -- The source for the stand-alone [FOLIO Developer's Curriculum](http://dev.folio.org/curriculum).

- [folio-org.github.io](https://github.com/folio-org/folio-org.github.io)
  -- The source for this dev.folio.org website.

