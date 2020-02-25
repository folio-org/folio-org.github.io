---
layout: page
title: Explain CQL string matching
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 2
---

See also [CQL in the Glossary](/reference/glossary/#cql) for further CQL information.

## CQL's exact match operator: ==

The CQL query `field == "abc xyz"` matches `abc xyz` only. It does not match either `The abc xyz` or `xyz abc` or `abc xyz.` or `abc, xyz`.

The SQL equivalent are `table.field = 'abc xyz'` and `table.field LIKE 'abc xyz'` (both are the same).

The CQL query `field == "abc xyz*"` has the SQL equivalent `table.field LIKE 'abc xyz%'`. This matches `abc xyz` and `abc xyz.` and `abc xyzq` and `abc xyz qqq`. It does not match either `The abc xyz` or `xyz abc` or `abc, xyz`. This is a left bounded match with right truncation.

The CQL query `field == "*abc xyz*"` has the SQL equivalent `table.field LIKE '%abc xyz%'`. This matches `abc xyz` and `abc xyz.` and `abc xyzq` and `abc xyz qqq` and `The abc xyz` and `The abc xyzq` and `The abc xyz qqq`. It does not match either `xyz abc` or `abc, xyz`. This is left and right truncation.

## CQL's word match operators: =, adj, all, any

The four word match operators ignore punctuation and whitespace, and they match against words. Truncation of a word is possible using the \* wildcard, but only on the right, not on the left.

It is implemented using [PostgreSQL's `to_tsvector @@ to_tsquery` full text search](https://www.postgresql.org/docs/current/functions-textsearch.html).

`all` matches if each word of the query string exists somewhere.

`any` matches if any word of the query string exists somewhere.

`adj` matches if all words of the query string exist consecutively in that order, there may be any whitespace and punctuation in between.

`=` is a synonym for `adj`.

Each of the CQL queries `field all "abc"`, `field any "abc"`, `field adj "abc"`, `field = "abc"` has the SQL equivalent `to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc')`. Each matches `abc` and `The abc xyz` and `?abc!xyz`. Each does not match `abcd`.

The CQL query `field all "abc xyz"` has the SQL equivalent `to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc & xyz')`. It matches `abc xyz` and `xyz abc` and `The abc xyz qqq` and `abc, xyz.`. It does not match `abc xyzq`.

The CQL query `field any "abc xyz"` has the SQL equivalent `to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc | xyz')`. It matches `abc` and `xyz` and `abc xyzq` and `abc xyz` and `abc, xyz.` and `xyz abc` and `The abc xyz qqq`. It does not match either `xyzq` or `qqq`.

The CQL query `field = "abc xyz"` has the SQL equivalent `to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc <-> xyz')`. It matches `abc xyz` and `The abc xyz qqq` and `abc, xyz.`. It does not match either `abc` or `xyz` or `xyz abc` or `abc xyzq`.

The CQL query `field = "abc*"` has the SQL equivalent `to_tsvector('simple', table.jsonb->>'field') @@ to_tsquery('simple', 'abc:*')`. It matches `abc` and `abcdef` and `The abcdef xyz` and `The!abcdef?xyz` and `xyz abc`. It does not match `xyzabc`.

