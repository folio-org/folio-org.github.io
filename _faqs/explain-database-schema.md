---
layout: page
title: Explain DB schema and performance issues
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: orientation
faqOrder: 10
---

*Q.* Data is stored in the database in [a form of JSON in JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html) fields within relational tables. At the same time framework generates queries like this

    SELECT  diku_mod_users.count_estimate_smart(
      'SELECT jsonb, id FROM diku_mod_users.users  WHERE (jsonb->>''id'') =  ''ba6baf95-bf14-4020-b44c-0cad269fb5c9''   ') AS count,  
           jsonb,
           id
     FROM diku_mod_users.users  
    WHERE (jsonb->>'id') =  'ba6baf95-bf14-4020-b44c-0cad269fb5c9'

And though this is a single row query it leads to a “full table scan” at the database level, which obviously has a great impact on performance. Also, I noticed that there were different values in `json.id` and `id` field and that confused me. And as for me, it doesn’t make sense to count rows in this case. Also joins will have a very bad performance because tables do not have foreign keys nor indexes for them.

*A.* From a performance standpoint, you can add indexes, FK, etc, as needed. There is no reason for a sequential (full table) scan to occur unless that is the fastest plan. We have run a lot of performance tests with millions of records (including the count estimate function, including joins between tables with millions of records) and have achieved very good performance (milliseconds) - system resource usage was also monitored during these tests. These performance tests have been run on the inventory module as it is the heaviest from a data standpoint (instances, items, holdings) - so optimizing smaller modules like users or permissions would not be an issue but I am not aware of the current performance status in those modules - but no doubt adding indexes will resolve probably any issue in those modules. Note that if a specific module is running a sequential scan where it should not, and an index is missing, then this may just be a bug that needs addressing and does not really have implications on the DB setup as a whole.

As a side note, I can say that there is massive work currently being done on [`cql2pgjson`](/folio-org/cql2pgjson-java) internals which should make querying much much faster so stay tuned for that.

*Q.* Framework does not cache prepared statements and does not use binding for SQL statements. This also has a huge impact on performance. And potentially there is a chance of SQL injection attacks if SQL binding is not used.

*A.* There are some prepared statements (saving and updating) but not for all and this should be addressed. However, note that the `cql2pgjson` module creates the entire `where` clause (this is our preferred method of work - using cql) - so in _most_ cases this is how the database is accessed [cql input ->> cql processed into an sql where clause (includes some validation) ->> where clause used to build full query].

*Q.* All data in the database in folio-stable has quite simple tabular form and I would prefer to redesign tables to the natural relational form and have in JSONB just additional information like user’s addresses and so on. Or maybe it makes sense to move back to [MongoDB](https://www.mongodb.com/).

*A.* Using Postgres gives us the ability to have a single DB technology with the flexibility to implement multiple methods of persisting data (if needed) with everything you would usually get from a relational DB. What added value does MongoDB provide that you feel is missing from the current jsonb implementation that would justify making a switch?
