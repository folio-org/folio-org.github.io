---
layout: page
title: Conduct cross-module joins via their APIs
permalink: /guides/cross-module-joins/
menuInclude: no
menuTopTitle: Guides
---

Database joins between different modules cannot be created at the SQL level, because you don't even know what other modules exist in the system, and you have no way of discovering what their tables and fields are even if you do know.
While it is true that the join on the DB-level would perform better, the down side of that approach across FOLIO would be tight coupling of modules and loss of replaceability and modularity.
A module's implementation details can change, and are shielded behind their reliable API, so all modules must be called via their well-known [APIs](/reference/api/).

FOLIO's microservice-like architecture facilitates [Decentralized Data Management and Polyglot Persistence](https://www.martinfowler.com/articles/microservices.html#DecentralizedDataManagement).

There are many examples for doing joins on the API level.
As one example, the "User Detail" screen shows Loans and other information gathered from various services.
Follow the code at [ui-users](https://github.com/folio-org/ui-users) and [mod-circulation-storage](https://github.com/folio-org/mod-circulation-storage).

Generally these operations should be fairly cheap, so a live look-up can be performed. For cases that require filter or search or sort by a specific datum that would be stored in another module, it probably makes sense to cache that datum locally in the calling module.

For back-end modules that utilise the RAML Module Builder framework, see the RMB documentation section
"[Querying multiple modules via HTTP](https://github.com/folio-org/raml-module-builder/blob/master/README.md#querying-multiple-modules-via-http)".
The framework blocks access from other modules by using a separate PostgreSQL role per module.

