---
layout: page
title: Explain DB schema and performance issues
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 2
---

*Q.* Data is stored in the database in [a form of JSON in JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html) fields within relational tables. At the same time framework generates queries like this

    SELECT  diku_mod_users.count_estimate_smart(
      'SELECT jsonb, id FROM diku_mod_users.users  WHERE (jsonb->>''id'') =  ''ba6baf95-bf14-4020-b44c-0cad269fb5c9''   ') AS count,
           jsonb,
           id
     FROM diku_mod_users.users
    WHERE (jsonb->>'id') =  'ba6baf95-bf14-4020-b44c-0cad269fb5c9'

And though this is a single row query it leads to a “full table scan” at the database level, which obviously has a great impact on performance. And as for me, it doesn’t make sense to count rows in this case. Also joins will have a very bad performance because tables do not have foreign keys nor indexes for them.

*A.* From a performance standpoint, you can add indexes, foreign keys, etc, as needed. There is no reason for a sequential (full table) scan to occur unless that is the fastest plan. The core development team has run a lot of performance tests with millions of records (including the count estimate function, including joins between tables with millions of records) and have achieved very good performance (milliseconds) - system resource usage was also monitored during these tests. These performance tests have been run on the inventory module as it is the heaviest from a data standpoint (instances, items, holdings) - so optimizing smaller modules like users or permissions would not be an issue. If there are issues, adding indexes will resolve probably any issue in those modules. Note that if a specific module is running a sequential scan where it should not, and an index is missing, then this may just be a bug that needs addressing and does not really have implications on the DB setup as a whole.

As a side note, there is massive work currently being done on [`cql2pgjson`](https://github.com/folio-org/cql2pgjson-java) internals which should make querying much much faster so stay tuned for that.

*Q.* Why exist both id and jsonb->>'id' in each table?

*A.* id is the PRIMARY KEY. PRIMARY KEY (and UNIQUE) and the foreign key constraint REFERENCES only work on a column, not on an expression like jsonb->>'id'. To ensure consistency a trigger copies id into jsonb->>'id' on each insert and update.

*Q.* Framework does not cache prepared statements and does not use binding for SQL statements. This also has a huge impact on performance. And potentially there is a chance of SQL injection attacks if SQL binding is not used.

*A.* There are some prepared statements (saving and updating) but not for all and this should be addressed. (Creating issues and pull requests to fix any such occurrences are welcome!)  However, note that the `cql2pgjson` module creates the entire `where` clause (this is our preferred method of work - using cql) - so in _most_ cases this is how the database is accessed [cql input ->> cql processed into an SQL where clause (includes some validation) ->> where clause used to build full query].

*Q.* All data in the databases in folio-stable has quite simple tabular form and I would prefer to redesign tables to the natural relational form and have in JSONB just additional information like user’s addresses and so on. Or maybe it makes sense to move back to [MongoDB](https://www.mongodb.com/).

*A.* Using Postgres gives us the ability to have a single database technology with the flexibility to implement multiple methods of persisting data (if needed) with everything you would usually get from a relational database.  This is in keeping with the vision of the FOLIO project to not be overly prescriptive in the technologies used by module developers while providing reasonable constraints to the reality of FOLIO implementations.
