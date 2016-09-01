---
layout: page
title: FOLIO Glossary
---

## FOLIO Components

### Okapi

The FOLIO middleware and API gateway. Okapi serves as the foundation
layer for managing FOLIO apps and services. For more information, see
the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).

### Stripes

The FOLIO UI toolkit. The Stripes toolkit provides a means of building
web applications that expose the functionality of underlying Okapi
modules. For more information, see the
[Stripes GitHub repository](https://github.com/folio-org/stripes-experiments).

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

### Docker

[Docker](https://www.docker.com) is a platform for managing software
containers. FOLIO is well-suited for deployment in a Docker
environment.

### JSON

JavaScript Object Notation
([JSON](https://en.wikipedia.org/wiki/JSON))
is an open-standard format that uses human-readable text to transmit
data objects consisting of attribute–value pairs.

### JWT

[JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token)
is a JSON-based open standard for creating tokens that assert some number
of claims. JWTs are authenticated and encrypted, and used by Okapi.

### Markdown

[Markdown](https://daringfireball.net/projects/markdown/) is a simple
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

[PostgresSQL](https://www.posgresql.org/) (often called "postgres") is
an open source enterprise-level relational database.

### RAML

[RESTful API Modeling Language](http://raml.org) - a language for the
definition of HTTP-based APIs. Okapi module APIs (including the API of
Okapi itself) are defined in RAML files and schemas.

### React

[React](https://facebook.github.io/react/)
is a JavaScript library for building user interfaces.

### Redux
[Redux](http://redux.js.org) is a state container for
JavaScript. Stripes uses React and Redux for building stateful
JavaScript web applications.

### Vert.x

[Vert.x](http://vertx.io) is a toolkit for building scalable, reactive
applications on the JVM. Vert.x is particularly suitable for
developing applications using the microservices architectural
pattern.

### Webpack

The Node.js module bundler, used to deploy Stripes modules.
