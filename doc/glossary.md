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

### Docker

[Docker](https://www.docker.com) is a platform for managing software
containers. FOLIO is well-suited for deployment in a Docker
environment.

### Microservices

A pattern for building loosely-coupled, highly available, modular
applications. Each component of a microservices-based application is a
self-contained service, which communicates with other component over
the network using a lightweight protocol. The FOLIO LSP is built using
a microservices architecture.

### Multitenant

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

### RAML

[RESTful API Modeling Language](http://raml.org) - a language for the
definition of HTTP-based APIs. Okapi module APIs (including the API of
Okapi itself) are defined in RAML files and schemas.

### Vert.x

[Vert.x](http://vertx.io) is a toolkit for building scalable, reactive
applications on the JVM. Vert.x is particularly suitable for
developing applications using the microservices architectural
pattern.

### Webpack

The Node.js module bundler, used to deploy Stripes modules.
