---
layout: source
title: Server Side Components
heading: Server Side Components
permalink: /source/serverside/
---

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
  The [API reference](/reference/reference) documentation is also
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

- [mod-login-saml](https://github.com/folio-org/mod-login-saml)
  -- Handles SAML login.
  
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

- [mod-notify](https://github.com/folio-org/mod-notify)
  -- Notifications to the users.
  
- [mod-acquisitions](https://github.com/folio-org/mod-acquisitions)
  -- Demo acquisitions module, based on the raml-module-builder framework,
  exposing acquisition APIs and objects against MongoDB.

- [mod-acquisitions-postgres](https://github.com/folio-org/mod-acquisitions-postgres)
  -- A second demo acquisitions module, also based on the
  raml-module-builder framework and exposing acquisition APIs and
  objects, but implemented with an asynchronous Postgres client.

