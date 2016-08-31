---
layout: page
title: Source Code
---

The FOLIO project includes server-side and client-side platform components, and
will grow to include library services that run on the platform.  All of the
code is located in several repositories in the GitHub organization,
[folio-org](https://github.com/folio-org).

A good starting point for exploring the code is
[Okapi](https://github.com/folio-org/okapi), specifically the [Okapi Guide and
Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md), which
introduces the concepts and architecture of the FOLIO platform, and includes
installation instructions and examples.  Okapi is the central hub for
applications running on the FOLIO platform and enables access to other modules
in the architecture.

## Server-side

Server-side elements, including _Okapi_, FOLIO "middleware" component, and additional services, frameworks and example modules.

[okapi](https://github.com/folio-org/okapi) -
Okapi API Gateway proxy/discovery/deployment service

[raml-module-builder](https://github.com/folio-org/raml-module-builder) -
framework allowing easy module creation based on raml files

[mod-circulation](https://github.com/folio-org/mod-circulation) -
circulation demo based on the raml-module-builder and a set of raml and json schemas representing some of the needed circulation functionality against a mongo DB

[mod-acquistions](https://github.com/folio-org/mod-acquisitions) -
demo acquisitions module exposing acq apis and objects based on the raml-module-builder framework against MongoDB

[mod-acquistions-postgres](https://github.com/folio-org/mod-acquisitions-postgres) -
demo acquisitions module exposing acq apis and objects based on the raml-module-builder framework implemented with async postgres client

[mod-configuration](https://github.com/folio-org/mod-configuration) -
demo configuration module based on the raml-module-builder and a set of raml and json schemas backed by a mongoDB async implementation

[mod-auth](https://github.com/folio-org/mod-auth) -
Prototype of a JWT auth module for FOLIO

[mod-metadata](https://github.com/folio-org/mod-metadata) -
Initial work on a Folio metadata store and related knowledge base / cataloguing concepts

## Client-side

Repositories related to Stripes, a  UI toolkit for FOLIO, still in the 
design phase.

[stripes-experiments](https://github.com/folio-org/stripes-experiments) -
Testing ground for prototype modules that may form part of Stripes.

[stripes-loader](https://github.com/folio-org/stripes-loader) -
Module loader to enable pluggable Redux applications.

[okapi-stripes](https://github.com/folio-org/stripes-loader) -
server-side module for generating UIs based on Stripes

## Other projects

[external-api-testing](https://github.com/folio-org/external-api-testing) -
Various tests of Okapi's APIs. 

