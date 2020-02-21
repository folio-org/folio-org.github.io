---
layout: page
title: Explain DB schema and performance issues
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 2
---

*Q.* Data is stored in the database in [a form of JSON in JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html) fields within relational tables. Why do some queries and joins result in a "full table scan"?

*A.* From a performance standpoint, you can add indexes, foreign keys, etc, as needed ([RMB Readme](https://github.com/folio-org/raml-module-builder/blob/master/README.md)). There is no reason for a sequential (full table) scan to occur unless that is the fastest plan. The core development team has run a lot of performance tests with millions of records (including the count estimate function, including joins between tables with millions of records) and have achieved very good performance (milliseconds) - system resource usage was also monitored during these tests. These performance tests have been run on the inventory module as it is the heaviest from a data standpoint (instances, items, holdings) - so optimizing smaller modules like users or permissions would not be an issue. If there are issues, adding indexes will resolve probably any issue in those modules. Note that if a specific module is running a sequential scan where it should not, and an index is missing, then this may just be a bug that needs addressing and does not really have implications on the DB setup as a whole.

*Q.* Why exist both `id` and `jsonb->>'id'` in each table?

*A.* id is the PRIMARY KEY. The PRIMARY KEY and the REFERENCES foreign key constraint only work on a column, not on an expression like `jsonb->>'id'`. To ensure consistency a [trigger](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/general_functions.ftl#L50) copies `id` into `jsonb->>'id'` on each insert and update.

*Q.* Why is each foreign key field like `statusId` copied into `jsonb->>'statusId'`?

*A.* PostgreSQL's REFERENCES foreign key constraint only works on a column, not on an expression like `jsonb->>'statusId'`. To ensure consistency a [trigger](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/foreign_keys.ftl#L25) copies `jsonb->>'statusId` into `statusId` on each insert and update.

*Q.* Are CQL queries fast when the `id` field or a foreign key field like `statusId` is used?

*A.* These fields are not converted into `jsonb->>'id'` or `jsonb->>'statusId'` but into the table columns `id` ([source code](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/cql2pgjson/src/main/java/org/folio/cql2pgjson/CQL2PgJSON.java#L712)) or `statusId` ([source code](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/cql2pgjson/src/main/java/org/folio/cql2pgjson/CQL2PgJSON.java#L723)). These columns automatically have an b-tree index because `id` is the PRIMARY KEY and RAML Module Builder (RMB) [adds](https://github.com/folio-org/raml-module-builder/blob/v29.2.2/domain-models-runtime/src/main/resources/templates/db_scripts/foreign_keys.ftl#L8-L9) the index for foreign key columns. This also ensures fast JOINs.

*Q.* Framework does not cache prepared statements and does not use binding for SQL statements. This also has a huge impact on performance. And potentially there is a chance of SQL injection attacks if SQL binding is not used.

*A.* There are some prepared statements (saving and updating) but not for all and this should be addressed. (Creating issues and pull requests to fix any such occurrences are welcome!)  However, note that the `cql2pgjson` module creates the entire `where` clause (this is our preferred method of work - using [CQL](/reference/glossary/#cql)) - so in _most_ cases this is how the database is accessed [cql input ->> cql processed into an SQL where clause (includes some validation) ->> where clause used to build full query].

*Q.* All data in the databases in folio-stable has quite simple tabular form and I would prefer to redesign tables to the natural relational form and have in JSONB just additional information like user’s addresses and so on. Or maybe it makes sense to move back to [MongoDB](https://www.mongodb.com/).

*A.* Using Postgres gives us the ability to have a single database technology with the flexibility to implement multiple methods of persisting data (if needed) with everything you would usually get from a relational database.  This is in keeping with the vision of the FOLIO project to not be overly prescriptive in the technologies used by module developers while providing reasonable constraints to the reality of FOLIO implementations.
