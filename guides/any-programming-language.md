---
layout: page
title: FOLIO uses any programming language
permalink: /guides/any-programming-language/
menuInclude: no
menuTopTitle: Guides
---

The design of FOLIO architecture
([microservices](/reference/glossary/#microservices) and [REST](/reference/glossary/#rest))
enables any module to be written in a programming language that the developer is comfortable with. So various programming languages and build environments could be utilized.

However, FOLIO has implemented a [Technical Designs and Decisions process](https://wiki.folio.org/display/DD/Technical+Designs+and+Decisions)
([presentation](https://docs.google.com/presentation/d/1y0xil4ThREq2mmuVtx1LxiPnvuGwVbBt65LV8EkU9zQ/edit?usp=sharing))
to provide consistency in FOLIO and to minimize the use of alternative tech stacks.

## Server-side

The [back-end](/source-code/#server-side) modules can utilize any language.

Frameworks abstract much functionality and enable the developer to focus on implementing business functions. Define the APIs and objects in RAML or OpenAPI files and schema files, then the framework generates code and provides tools to help implement the module. Frameworks currently in use:

* [raml-module-builder](https://github.com/folio-org/raml-module-builder) (RMB) for RAML files and Vert.x
* [folio-vertx-lib](https://github.com/folio-org/folio-vertx-lib) for OpenAPI files and Vert.x
* [Spring Way](https://docs.google.com/presentation/d/1YgDCBimLTQ1ou-fPhvyKbWpVkec3Goa8lyJJe2hcLHk/edit) for OpenAPI files and Spring based Java

Key requirements for server-side modules:

* Be able to handle the REST interactions according to the [API](/reference/api/) and implement the lifecycle endpoints.
* As [explained](https://github.com/folio-org/okapi/blob/master/doc/guide.md#chunked) in the Okapi Guide, Okapi uses HTTP 1.1 with chunked encoding to make the connections to the modules.

## Client-side

The [front-end](/source-code/#client-side) user interface code can be written using any toolkit and programming language, since Okapi represents all of the FOLIO functionality as well-behaved web services.
FOLIO provides the [Stripes](/source-code/#client-side) UI toolkit (JavaScript), optimized for accessing Okapi-based services and wrapping UI functionality into convenient modules.

* Be able to handle the REST interactions according to the [API](/reference/api/).
* Be able to manage state and send special headers such as X-Okapi-Tenant.

## Current situation

So far we have concentrated on server-side modules in Java using Vert.x or Spring, and
client-side in Node.js and React. Because we use them internally, those technologies will have
a prominent place in the FOLIO ecosystem and, initially, it may be easiest
to get started using them. We provide libraries and utilities that
help with development (especially with writing standard boiler-plate code and
scaffolding).

