---
layout: page
title: Explain CQL string matching
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 3
---

See also [CQL in the Glossary](/reference/glossary/#cql) and RAML Module Builder's
[CQL](https://github.com/folio-org/raml-module-builder#cql-relations),
[CQL2PgJSON](https://github.com/folio-org/raml-module-builder#cql2pgjson-multi-field-index),
and [Post Tenant (schema.json)](https://github.com/folio-org/raml-module-builder#the-post-tenant-api)
documentation sections for further CQL information.

See explanations and examples below for
[Field match operator](#field) and [Word match operators](#word).

## Field match operator: == {#field}{#exact}

The CQL "exact match" operator (`==`) is used to match against a complete field.

Truncation is enabled using the \* wildcard, either on the right end or on the left end.

If the `==` search is to be accelerated, then create a B-tree database index by
adding an `"index"` or `"uniqueIndex"` entry for the field in `schema.json`
as explained in
[RAML Module Builder Post Tenant API documentation](https://github.com/folio-org/raml-module-builder#the-post-tenant-api).

Only right end truncation is supported by B-tree database indexes.

### Field match examples 1 {#field-examples-1}{#exact-examples-1}

Consider the CQL query:
```
field == "abc xyz"
```

It does match only:
```
abc xyz
```

It does not match:
```
The abc xyz
xyz abc
abc xyz.
abc, xyz
```

This has the SQL equivalents (both are the same):<br/>
`table.field = 'abc xyz'`<br/>
`table.field LIKE 'abc xyz'`

### Field match examples 2 {#field-examples-2}{#exact-examples-2}

Consider the CQL query:
```
field == "abc xyz*"
```

This is a left bounded match with right truncation.

It does match:
```
abc xyz
abc xyz.
abc xyzq
abc xyz qqq
```

It does not match:
```
The abc xyz
xyz abc
abc, xyz
```

This has the SQL equivalent:<br/>
`table.field LIKE 'abc xyz%'`

### Field match examples 3 {#field-examples-3}{#exact-examples-3}

Consider the CQL query:
```
field == "*abc xyz*"
```
This is left and right truncation.

It does match:
```
abc xyz
abc xyz.
abc xyzq
abc xyz qqq
The abc xyz
The abc xyzq
The abc xyz qqq
```

It does not match:
```
xyz abc
abc, xyz
```

This has the SQL equivalent:<br/>
`table.field LIKE '%abc xyz%'`

Note that this is slow on large datasets because b-tree database indexes
support only right truncation.

## Word match operators: =, adj, all, any {#word}

The four word match operators ignore punctuation and whitespace, and they match against words.

Truncation of a word is possible using the \* wildcard, but only on the right, not on the left.

It is implemented using [PostgreSQL's `to_tsvector @@ to_tsquery` full text search](https://www.postgresql.org/docs/current/functions-textsearch.html).

`all` matches if each word of the query string exists somewhere.

`any` matches if any word of the query string exists somewhere.

`adj` matches if all words of the query string exist consecutively in that order, there may be any whitespace and punctuation in between.

`=` is a synonym for `adj`.

If a word match search is to be accelerated, then create a full text database index by
adding a `"fullTextIndex"` entry for the field in `schema.json`
as explained in
[RAML Module Builder Post Tenant API documentation](https://github.com/folio-org/raml-module-builder#the-post-tenant-api).

Only right end truncation is supported by word match operators and full text database indexes.

### Word match examples 1 {#word-examples-1}

Consider each of the CQL queries:
```
field all "abc"
field any "abc"
field adj "abc"
field = "abc"
```

Each does match:
```
abc
The abc xyz
?abc!xyz
```

Each does not match:
```
abcd
```

These have the SQL equivalent:<br/>
`to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc')`

### Word match examples 2 {#word-examples-2}

Consider the CQL query:
```
field all "abc xyz"
```

It does match:
```
abc xyz
xyz abc
The abc xyz qqq
abc, xyz.
```

It does not match:
```
abc xyzq
```

This has the SQL equivalent:<br/>
`to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc & xyz')`

### Word match examples 3 {#word-examples-3}

Consider the CQL query:
```
field any "abc xyz"
```

It does match:
```
abc
xyz
abc xyzq
abc xyz
abc, xyz.
xyz abc
The abc xyz qqq
```

It does not match:
```
xyzq
qqq
```

This has the SQL equivalent:<br/>
`to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc | xyz')`

### Word match examples 4 {#word-examples-4}

Consider the CQL query:
```
field = "abc xyz"
```

It does match:
```
abc xyz
The abc xyz qqq
abc, xyz.
```

It does not match:
```
abc
xyz
xyz abc
abc xyzq
```

This has the SQL equivalent:<br/>
`to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc <-> xyz')`

### Word match examples 5 {#word-examples-5}

Consider the CQL query:
```
field = "abc*"
```

It does match:
```
abc
abcdef
The abcdef xyz
The!abcdef?xyz
xyz abc
```

It does not match:
```
xyzabc
```

This has the SQL equivalent:<br/>
`to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc:*')`

