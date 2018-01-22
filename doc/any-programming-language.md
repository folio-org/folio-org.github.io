---
layout: page
title: FOLIO uses any programming language
permalink: /doc/any-programming-language/
menuInclude: no
menuTopTitle: Documentation
---

The design of FOLIO architecture
([microservices](/doc/glossary#microservices) and [REST](/doc/glossary#rest))
enables any module to be written in a programming language that the developer is comfortable with. So various programming languages and build environments can be utilized.

## Server-side

The [back-end](/source-code/#server-side) modules can utilize any language.
The [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework, is a special module that abstracts much functionality and enables the developer to focus on implementing business functions. Define the APIs and objects in RAML files and schema files, then the RMB generates code and provides tools to help implement the module.
Note that at this stage of the FOLIO project, only this Java-based framework is available.
Other frameworks would be possible.

* Be able to handle the REST interactions according to the [API](/doc/api/) and implement the lifecycle endpoints.
* As [explained](https://github.com/folio-org/okapi/blob/master/doc/guide.md#chunked) in the Okapi Guide, Okapi uses HTTP 1.1 with chunked encoding to make the connections to the modules.

## Client-side

The [front-end](/source-code/#client-side) user interface code can be written using any toolkit and programming language, since Okapi represents all of the FOLIO functionality as well-behaved web services.
FOLIO provides the [Stripes](/source-code/#client-side) UI toolkit (JavaScript), optimized for accessing Okapi-based services and wrapping UI functionality into convenient modules.
Other toolkits would be possible.

* Be able to handle the REST interactions according to the [API](/doc/api/).
* Be able to manage state and send special headers such as X-Okapi-Tenant.

## Current situation

So far we have concentrated on server-side modules in Java using Vert.x, and
client-side in Node.js and React. Because we use them internally, those technologies will have
a prominent place in the FOLIO ecosystem and, initially, it may be easiest
to get started using them. We provide libraries and utilities that
help with development (especially with writing standard boiler-plate code and
scaffolding) but we hope to eventually gain a wide coverage among other
tools and technologies (e.g. Python, Ruby, etc.). We are counting on an active
engagement from the community to help out in this area.

