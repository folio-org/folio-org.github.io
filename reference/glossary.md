---
layout: page
title: FOLIO Glossary
permalink: /reference/glossary/
menuInclude: yes
menuTopTitle: Reference
menuSubTitle: Glossary
menuSubIndex: 4
---

FOLIO is a new open source, cloud hostable, app-store based library platform,
designed to facilitate collaboration between disparate development teams.

This glossary defines some terms to assist developers.
Some other relevant documents are:
[Acronyms](https://wiki.folio.org/display/PC/Acronyms),
[Glossary](https://wiki.folio.org/display/PC/Glossary+of+Terms).

## FOLIO Components

### Okapi

The FOLIO middleware and API gateway. Okapi serves as the foundation
layer for managing FOLIO apps and services. For more information, see
the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).

### Stripes

The FOLIO UI toolkit. The Stripes toolkit provides a means of building
web applications that expose the functionality of underlying Okapi
modules. For more information, see the
[Stripes Core GitHub repository](https://github.com/folio-org/stripes-core).

### Stripes entities

The document
[Stripes entities: packages, modules, apps and more](https://github.com/folio-org/stripes-core/blob/master/doc/modules-apps-etc.md)
is a summary of terms used in that context, e.g. component, package, module, app, plugin.

## FOLIO Technologies and Concepts

### API

Application programming interfaces
([APIs](https://en.wikipedia.org/wiki/Application_programming_interface))
are well-defined interfaces through which interactions happen.

### App Store

An online portal for obtaining and installing software. FOLIO is
designed to support the installation of both free and commercial
modules and applications through an App Store.

### AWS/ECS

[Amazon Web Services](https://aws.amazon.com/) and the
[Amazon EC2 Container Service](https://aws.amazon.com/ecs/) is a
cloud-based application deployment platform from Amazon. FOLIO is
designed to play well in the cloud.

### BIBFRAME

Bibliographic Framework Initiative
([BIBFRAME](https://en.wikipedia.org/wiki/BIBFRAME)).

### CQL

Contextual Query Language
([CQL](https://en.wikipedia.org/wiki/Contextual_Query_Language)).
It was previously known as Common Query Language,
and that is not to be confused with the
[OGC](http://docs.geoserver.org/latest/en/user/tutorials/cql/cql_tutorial.html)
language of the same name.

Some starting points are:

- [A Gentle Introduction to CQL](http://zing.z3950.org/cql/intro.html).
- FOLIO [CQL to PostgreSQL JSON converter](https://github.com/folio-org/cql2pgjson-java) in Java.
- The [CQL-1.2](http://www.loc.gov/standards/sru/cql/) specification and context sets.
- As [SRU](#sru) 2.0 is OASIS searchRetrieve Version 1.0, then CQL is its
  [Part 5](http://docs.oasis-open.org/search-ws/searchRetrieve/v1.0/os/part5-cql/searchRetrieve-v1.0-os-part5-cql.html).
- [CQL-Java](http://www.indexdata.com/cql-java).
- The CQL parser in [YAZ](http://www.indexdata.com/yaz/doc/tools.html#cql).

A CQL example:
```
(username=="ab*" or personal.firstName=="ab*" or personal.lastName=="ab*")
and active=="true" sortby personal.lastName personal.firstName barcode
```

For other relevant CQL examples see the first two items above, and the [API docs](/reference/api/), and the debug output for tests in each backend module.

### Docker

[Docker](https://www.docker.com) is a platform for managing software
containers. FOLIO is well-suited for deployment in a Docker
environment.

### DRY

Don't repeat yourself
([DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)).

### ECMAScript

[ECMAScript](https://en.wikipedia.org/wiki/ECMAScript)
is the formally standardised version JavaScript.
The Stripes Toolkit is written in
[ES6](http://es6-features.org/),
a modern variant that introduces several new facilities.

### FRBR

Functional Requirements for Bibliographic Records
([FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records)).

### ILS

Integrated Library System
([ILS](https://en.wikipedia.org/wiki/Integrated_library_system)).

### JSON

JavaScript Object Notation
([JSON](https://en.wikipedia.org/wiki/JSON))
is an open-standard format that uses human-readable text to transmit
data objects consisting of lists, collections and attribute–value pairs.

### JWT

[JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token)
is a JSON-based open standard for creating tokens that assert some number
of claims. JWTs are authenticated and encrypted, and used by Okapi.

### LSP

Library Services Platform (LSP).

### MARC

[MARC](https://en.wikipedia.org/wiki/MARC_standards)
(Machine-Readable Cataloging) standards.

### Markdown

[Markdown](https://en.wikipedia.org/wiki/Markdown) is a simple
plain text formatting syntax, used for documentation throughout the
FOLIO code.

### MongoDB

[MongoDB](https://www.mongodb.com/) is an open source, schemaless
document database.

### Microservices

A pattern for building loosely-coupled, highly available, modular
applications. Each component of a microservices-based application is a
self-contained service, which communicates with other components over
the network using a lightweight protocol. The FOLIO LSP is built using
a microservices architecture.

### Multitenancy

A pattern of software architecture in which a single instance of the
software is designed to serve multiple tenants, with appropriate
security provisions and data separation. FOLIO is designed from the
ground up to operate in a multitenant environment.

### NCIP

NISO Circulation Interchange Protocol
([NCIP](http://www.ncip.info/introduction-to-ncip.html)).

### Node.js

[Node.js](https://nodejs.org) is a JavaScript runtime for deploying
JavaScript code.

### NPM

The Node.js Node Package Manager - a mechanism for distributing
packages of JavaScript code, used by Stripes.

### OLE

The [Open Library Environment](https://www.openlibraryenvironment.org/)
is a community of academic and research libraries collaborating to
build open source library management tools. OLE has joined the FOLIO
community to help with the development of FOLIO.

### PostgreSQL

[PostgreSQL](https://www.postgresql.org/) (often called "Postgres") is
an open source enterprise-level relational database.

### PoC

Proof-of-concept
([PoC](https://en.wikipedia.org/wiki/Proof_of_concept))

### RAML

[RESTful API Modeling Language](http://raml.org) - a language for the
definition of HTTP-based APIs. Okapi module APIs (including the API of
Okapi itself) are defined in RAML files and schemas.

### RDA

Resource Description and Access
([RDA](https://en.wikipedia.org/wiki/Resource_Description_and_Access)).

### React

[React](https://facebook.github.io/react/)
is a JavaScript library for building user interfaces.

### Redux
[Redux](http://redux.js.org) is a state container for
JavaScript. Stripes uses React and Redux for building stateful
JavaScript web applications.

### REST

Representational State Transfer architectural style, and RESTful web services, enable interaction between systems using a well-known set of stateless operations and responses.

### RMB

The [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework, is a special FOLIO module that abstracts much functionality and enables the developer to focus on implementing business functions.

### Solr

[Apache Solr](https://en.wikipedia.org/wiki/Apache_Solr).

### SRU

Search/Retrieve via URL
([SRU](http://www.loc.gov/standards/sru/)).
Version "[SRU 2.0](http://www.loc.gov/standards/sru/sru-2-0.html)"
is "searchRetrieve Version 1.0, OASIS Standard".

### Vert.x

[Vert.x](http://vertx.io) is a toolkit for building scalable, reactive
applications on the JVM. Vert.x is particularly suitable for
developing applications using the microservices architectural
pattern.

### Webpack

The Node.js module bundler, used to deploy Stripes modules.

### Z39.50

[Z39.50](https://en.wikipedia.org/wiki/Z39.50)
refers to ANSI/NISO standard Z39.50, and ISO standard 23950
"Information Retrieval (Z39.50): Application Service Definition and Protocol Specification".
The Library of Congress is the
[Z39.50 Maintenance Agency](http://www.loc.gov/z3950/agency/).
