---
layout: page
title: Explain CQL string matching
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 2
---

See also [CQL in the Glossary](/reference/glossary/#cql) for further CQL information.

## Exact match operator: == {#exact}

### Exact match examples 1 {#exact-examples-1}

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

### Exact match examples 2 {#exact-examples-2}

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

### Exact match examples 3 {#exact-examples-3}

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

## Word match operators: =, adj, all, any {#word}

The four word match operators ignore punctuation and whitespace, and they match against words. Truncation of a word is possible using the \* wildcard, but only on the right, not on the left.

It is implemented using [PostgreSQL's `to_tsvector @@ to_tsquery` full text search](https://www.postgresql.org/docs/current/functions-textsearch.html).

`all` matches if each word of the query string exists somewhere.

`any` matches if any word of the query string exists somewhere.

`adj` matches if all words of the query string exist consecutively in that order, there may be any whitespace and punctuation in between.

`=` is a synonym for `adj`.

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

