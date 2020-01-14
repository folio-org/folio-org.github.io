---
layout: page
title: How to check for a valid UUID
permalink: /guides/uuids/
menuInclude: no
menuTopTitle: Guides
---

The regexp
`^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[1-5][a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$`
matches any valid UUID. This accepts v1, v2, v3, v4 and v5 UUIDs as FOLIO allows all of them,
but it excludes the Nil UUID `00000000-0000-0000-0000-000000000000` that usually serves as a
NullObject to be used for the Null Object Pattern.

A UUID has the form xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx where the version M must be [1-5]
and the variant N must be [89abAB]

The shared `raml-util` repository has [schemas/uuid.schema](https://github.com/folio-org/raml/blob/raml1.0/schemas/uuid.schema) for UUID verification.

See also
[UUID at Wikipedia](https://en.wikipedia.org/wiki/Universally_unique_identifier).

