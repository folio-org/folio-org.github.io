---
layout: page
title: Explain DB schema and performance issues
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 4
---

*Q.* Data is stored in the database in [a form of JSON in JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html) fields within relational tables. Why do some queries and joins result in a "full table scan"?

*A.* From a performance standpoint, you can add indexes, foreign keys, etc, as needed ([RMB Readme](https://github.com/folio-org/raml-module-builder/blob/master/README.md)). There is no reason for a sequential (full table) scan to occur unless that is the fastest plan. The core development team has run a lot of performance tests with millions of records (including the count estimate function, including joins between tables with millions of records) and have achieved very good performance (milliseconds) - system resource usage was also monitored during these tests. These performance tests have been run on the inventory module as it is the heaviest from a data standpoint (instances, items, holdings) - so optimizing smaller modules like users or permissions would not be an issue. If there are issues, adding indexes will resolve probably any issue in those modules. Note that if a specific module is running a sequential scan where it should not, and an index is missing, then this may just be a bug that needs addressing and does not really have implications on the DB setup as a whole.
(The Wiki [FOLIOtips/Searching](https://wiki.folio.org/display/FOLIOtips/Searching) has further notes about search indexes, and adding indexes for an RMB-based module via its `db_scripts/schema.json` file.)

*Q.* Why exist both `id` and `jsonb->>'id'` in each table?

*A.* id is the PRIMARY KEY. The PRIMARY KEY and the REFERENCES foreign key constraint only work on a column, not on an expression like `jsonb->>'id'`. To ensure consistency a [trigger](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/general_functions.ftl#L50) copies `id` into `jsonb->>'id'` on each insert and update.

*Q.* Why is each foreign key field like `statusId` copied into `jsonb->>'statusId'`?

*A.* PostgreSQL's REFERENCES foreign key constraint only works on a column, not on an expression like `jsonb->>'statusId'`. To ensure consistency a [trigger](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/foreign_keys.ftl#L25) copies `jsonb->>'statusId` into `statusId` on each insert and update.

*Q.* Are CQL queries fast when the `id` field or a foreign key field like `statusId` is used?

*A.* These fields are not converted into `jsonb->>'id'` or `jsonb->>'statusId'` but into the table columns `id` ([source code](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/cql2pgjson/src/main/java/org/folio/cql2pgjson/CQL2PgJSON.java#L712)) or `statusId` ([source code](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/cql2pgjson/src/main/java/org/folio/cql2pgjson/CQL2PgJSON.java#L723)). These columns automatically have an b-tree index because `id` is the PRIMARY KEY and RAML Module Builder (RMB) [adds](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/foreign_keys.ftl#L8-L9) the index for foreign key columns. This also ensures fast JOINs.

*Q.* Does putting the fields into a JSONB column increase the risk of data collisions?

*A.* No, because PostgreSQL doesn't have column-level locks, it has only [row-level locks](https://www.postgresql.org/docs/current/mvcc.html). Both `UPDATE t SET a = "foo"` and `UPDATE t SET jsonb = jsonb || '{"a": "foo"}'` have the same risk of collision with updates of other transactions. Both can make use of row-level locking using `SELECT FOR UPDATE`, and both need to use [Optimistic Locking](https://wiki.folio.org/display/DD/Optimistic+locking+support) for workflows without transactions, for example when a human edits a record in the browser.

*Q.* Framework does not cache prepared statements and does not use binding for SQL statements. This also has a huge impact on performance. And potentially there is a chance of SQL injection attacks if SQL binding is not used.

*A.* RMB Framework uses binding for SQL statements wherever possible ([data binding code review](https://issues.folio.org/browse/RMB-189)). You are [welcome to report](https://wiki.folio.org/display/SEC/FOLIO+Vulnerability+and+Remediation+Policy) any issue you find. However, note that the [cql2pgjson](https://github.com/folio-org/raml-module-builder/tree/master/cql2pgjson) sub-module creates the entire `WHERE` clause, so in _many_ cases this is how the database is accessed: [CQL](/reference/glossary/#cql) input is converted into an SQL `WHERE` clause that is used to build the full query ([CQL-to-SQL code review](https://issues.folio.org/browse/RMB-565)). We can easily change the code to cache a prepared statement if there is a need, however, we don't know of any query where this gives us a significant performance boost -- please share the findings of your performance tests!

*Q.* Is there a default implementation for standard APIs?

*A.* Yes: [PgUtil](https://github.com/folio-org/raml-module-builder/blob/v32.0.0/domain-models-runtime/src/main/java/org/folio/rest/persist/PgUtil.java). Example usage: [BoundWithPartAPI.java](https://github.com/folio-org/mod-inventory-storage/blob/v21.0.0/src/main/java/org/folio/rest/impl/BoundWithPartAPI.java).

*Q.* Why can't a module directly access the database tables of other modules?

*A.* Each module has a separate [database schema](https://www.postgresql.org/docs/current/ddl-schemas.html) to enforce that access always goes via APIs. Okapi rejects any user and any module that doesn't have sufficient permissions to call that API. We don't want to duplicate the sophisticated permission checks in the database. FOLIO is designed to allow a tenant to enable a module that is closed source or has low quality for a single tenant. If the module runs in a separate database schema and needs to go via APIs it can only do any harm to other modules if permissions to write to these other modules are declared in the module's ModuleDescriptor, and restricted to this tenant's data. This is similar to mobile phone apps where the weather app is not allowed to access photos and emails. Separating modules by APIs also enforces development teams to clearly declare their APIs and the inter-module dependencies. This enforces good documentation, good architecture and greatly helps to coordinate FOLIO's many development teams.

*Q.* Can modules share PostgreSQL extensions securely?

*A.* A module must load a PostgreSQL extension using `CREATE EXTENSION IF NOT EXISTS extension_name WITH SCHEMA public`. Using schema public is required for sharing the extension, because an extension can be loaded only once per database. Loading the extension's objects into a module specific database blocks all other modules from using the extension. Using schema public is secure because schema public is not in the `search_path`. For details see [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) and [Schema Usage Patterns](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATTERNS) in the PostgreSQL documentation.

*Q.* All data in the databases in folio-stable has quite simple tabular form and I would prefer to redesign tables to the natural relational form and have in JSONB just additional information like user’s addresses and so on. Or maybe it makes sense to move back to [MongoDB](https://www.mongodb.com/).

*A.* Using Postgres gives us the ability to have a single database technology with the flexibility to implement multiple methods of persisting data (if needed) with everything you would usually get from a relational database.  This is in keeping with the vision of the FOLIO project to not be overly prescriptive in the technologies used by module developers while providing reasonable constraints to the reality of FOLIO implementations.

