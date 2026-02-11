---
layout: page
title: FOLIO Glossary
permalink: /reference/glossary/
menuInclude: yes
menuTopTitle: Reference
menuSubTitle: Glossary
menuSubIndex: 6
---

FOLIO is a new open source, cloud hostable, app-store based library platform,
designed to facilitate collaboration between disparate development teams.

This glossary defines some terms to assist developers.

Some other relevant documents are:
[Acronyms](https://wiki.folio.org/display/PC/Acronyms),
[Glossary](https://docs.google.com/document/d/1c2NkqJ0amsorBBWB8MuvSqXaQSIwqhL4t3i2zxEFR5I),
[Glossary](https://wiki.folio.org/display/PC/Glossary+of+Terms),
[Glossary](https://wiki.folio.org/display/FOLIOtips/Glossary),
[Glossary](https://docs.folio.org/docs/glossary/).

## FOLIO Components

### Okapi

The FOLIO middleware and API gateway. Okapi serves as the foundation
layer for managing FOLIO apps and services. For more information, see
the [Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).

### Stripes

The FOLIO UI toolkit. The Stripes toolkit provides a means of building
web applications that expose the functionality of underlying Okapi
modules. For more information, see the
[Stripes GitHub repository](https://github.com/folio-org/stripes).

### Stripes entities

The document
[Stripes entities: packages, modules, apps and more](https://github.com/folio-org/stripes/blob/master/doc/modules-apps-etc.md)
is a summary of terms used in that context, e.g. component, package, module, app, plugin.

### Okapi-Stripes Platform, LSP Base, LSP Extended

The "Okapi-Stripes Platform" and the "FOLIO LSP Base" and the "FOLIO LSP Extended Apps" are [defined](https://folio-org.atlassian.net/wiki/x/CxJN).

## FOLIO Special Interest Groups (SIGs) {#sigs}

For further information about SIGs and how to participate, refer to [Special Interest Groups](https://wiki.folio.org/display/PC/Special+Interest+Groups).

Some abbreviations are provided below. Note that there are other SIGs besides these.

### A11Y {#sig-a11y}

Accessibility

### CO {#sig-co}

Community Outreach

### DM {#sig-dm}

Data Migration

### LDP {#sig-ldp}

Library Data Platform - Reporting

### MM {#sig-mm}

Metadata Management

### RA {#sig-ra}

Resource Access

### RM {#sig-rm}

Resource Management

### SO {#sig-so}

SysOps

### UM {#sig-um}

User Management

## FOLIO Technologies and Concepts

### Terms A-F

#### a11y

Accessibility. Refer to
the FOLIO [A11Y SIG](https://folio-org.atlassian.net/wiki/spaces/A11Y/overview)
and [Accessibility in Stripes](https://folio-org.github.io/stripes-components/?path=/docs/guides-accessibility-accessibility-overview--docs)
and [The A11Y Project](https://www.a11yproject.com/).

#### API

Application programming interfaces
([APIs](https://en.wikipedia.org/wiki/Application_programming_interface))
are well-defined interfaces through which interactions happen.

#### App Store

An online portal for obtaining and installing software. FOLIO is
designed to support the installation of both free and commercial
modules and applications through an App Store.

#### AWS/ECS

[Amazon Web Services](https://aws.amazon.com/) and the
[Amazon EC2 Container Service](https://aws.amazon.com/ecs/) is a
cloud-based application deployment platform from Amazon. FOLIO is
designed to play well in the cloud.

#### BIBFRAME

Bibliographic Framework Initiative
([BIBFRAME](https://en.wikipedia.org/wiki/BIBFRAME)).

#### CC

The [FOLIO Community Council](https://wiki.folio.org/display/CC/)

#### CQL

Contextual Query Language
([CQL](https://en.wikipedia.org/wiki/Contextual_Query_Language)).
It was previously known as Common Query Language,
and that is not to be confused with the
[OGC](https://docs.geoserver.org/latest/en/user/tutorials/cql/cql_tutorial.html)
language of the same name.

Some starting points are:

- [A Gentle Introduction to CQL](http://zing.z3950.org/cql/intro.html) (incomplete, outdated, explains features not supported by FOLIO).
- FOLIO [CQL to PostgreSQL JSON converter](https://github.com/folio-org/raml-module-builder#cql-contextual-query-language) (CQL2PgJSON).
- FOLIO FAQ [Explain CQL string matching](/faqs/explain-cql/)
- The [CQL-1.2](https://www.loc.gov/standards/sru/cql/) specification and context sets.
- As [SRU](#sru) 2.0 is OASIS searchRetrieve Version 1.0, then CQL is its
  [Part 5](https://docs.oasis-open.org/search-ws/searchRetrieve/v1.0/os/part5-cql/searchRetrieve-v1.0-os-part5-cql.html).
- [CQL-Java](https://www.indexdata.com/resources/software/cql-java/).
- The CQL parser in [YAZ](https://software.indexdata.com/yaz/doc/tools.html#cql).

A CQL example:
```
(username=="ab*" or personal.firstName=="ab*" or personal.lastName=="ab*")
and active=="true" sortby personal.lastName personal.firstName barcode
```

For other relevant CQL examples see the FOLIO items above, and the [API docs](/reference/api/), and the debug output for tests in each backend module.

#### CO

[Code Owner](/guidelines/development-design-review/#code-owner-co).

#### CRUD

The basic functions of persistent storage: Create, Read, Update, Delete ([CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)).

#### CSP

[Critical Service Patch](https://wiki.folio.org/display/REL/Critical+Service+Patch+Process) (CSP).

#### DevOps

Combining software development and information technology operations:
[DevOps](https://en.wikipedia.org/wiki/DevOps).

#### Docker

[Docker](https://www.docker.com) is a platform for managing software
containers. FOLIO is well-suited for deployment in a Docker
environment.

#### DoD

Definition of Done (DoD).
Criteria to decide when a feature is deemed finished, and its issue tracker tickets are closed.
Refer to the [management](/guidelines/#development-management) notes for each FOLIO Development Team.

#### DoR

Definition of Ready (DoR).
Criteria to decide when a feature is well-described and is deemed ready to be scheduled to undertake the work.
Refer to the [management](/guidelines/#development-management) notes for each FOLIO Development Team.

#### DR

[Decision Records](https://wiki.folio.org/display/TC/Decision+Records) (DR) -- The collection of ADRs (Architectural Decision Records) is referred to as ADL (Architecture Decision Log).

#### DRY

Don't repeat yourself
([DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)).

#### ECMAScript

[ECMAScript](https://en.wikipedia.org/wiki/ECMAScript)
is the formally standardised version of JavaScript.
The Stripes Toolkit is written in
[ES6](http://es6-features.org/),
a modern variant that introduces several new facilities.

#### EKS

Amazon Elastic Kubernetes Service ([Amazon EKS](https://aws.amazon.com/eks/)).

#### ERM

Electronic resource management ([ERM](https://en.wikipedia.org/wiki/Electronic_resource_management)).

#### FOLIO

FOLIO -- The Future of Libraries is Open.

The term "FOLIO" is an acronym, and must always be noted as an upper-case word.
Refer to the "FOLIO Brand Identity Guidelines" document at [FOLIO Graphics and Branding Resources](https://folio-org.atlassian.net/wiki/x/UAQg).

#### FRBR

Functional Requirements for Bibliographic Records
([FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records)).

### Terms G-M

#### HOC

"Higher-order components" are a pattern for re-use of component logic with [React](#react).

#### HRID

Human-readable identifier (HRID) is an additional unique identifier available on some records.
Also known as eye-readble identifier.
Not to be confused with the [UUID](#uuid) of a holdings record (which may also have a HRID).

#### ILS

Integrated Library System
([ILS](https://en.wikipedia.org/wiki/Integrated_library_system)).

#### JSON

JavaScript Object Notation
([JSON](https://en.wikipedia.org/wiki/JSON))
is an open-standard format that uses human-readable text to transmit
data objects consisting of lists, collections and attribute–value pairs.

#### JSON Schema

Vocabularies that [define](/start/primer-raml/) the format of JSON instances.

#### JWT

[JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token)
is a JSON-based open standard for creating tokens that assert some number
of claims. JWTs are authenticated and encrypted, and used by Okapi.

#### Kafka

[Apache Kafka](https://kafka.apache.org/) is a distributed event streaming platform.

#### Kubernetes

[Kubernetes](https://en.wikipedia.org/wiki/Kubernetes) (k8s) is a
"platform for automating deployment, scaling, and operations of application containers across clusters of hosts".

#### LDP

Library Data Platform ([LDP](https://github.com/library-data-platform)) is an open source platform for reporting and analytics in libraries.

#### LM

[Lead Maintainer](/guidelines/development-design-review/#lead-maintainer-lm).

#### LSP

Library Services Platform (LSP).

#### LTI

Learning Tools Interoperability
([LTI](https://en.wikipedia.org/wiki/Learning_Tools_Interoperability)).

#### MARC

[MARC](https://en.wikipedia.org/wiki/MARC_standards)
(Machine-Readable Cataloging) standards.

#### Markdown

[Markdown](https://en.wikipedia.org/wiki/Markdown) is a simple
plain text formatting syntax, used for documentation throughout the
FOLIO code.

#### MFHD

MARC 21 Format for Holdings Data ([MFHD](https://www.loc.gov/marc/holdings/)).

#### MongoDB

[MongoDB](https://www.mongodb.com/) is an open source, schemaless
document database.

#### Microservices

A pattern for building loosely-coupled, highly available, modular
applications. Each component of a microservices-based application is a
self-contained service, which communicates with other components over
the network using a lightweight protocol. The FOLIO LSP is built using
a microservices architecture.

#### Multitenancy

A pattern of software architecture in which a single instance of the
software is designed to serve multiple tenants, with appropriate
security provisions and data separation. FOLIO is designed from the
ground up to operate in a multitenant environment.

#### MVP

Market-Viable Platform (MVP).
Refer to the [FOLIO Implementers SIG](https://wiki.folio.org/display/COHORT2019/FOLIO+Implementers+SIG).

### Terms N-R

#### NCIP

NISO Circulation Interchange Protocol
([NCIP](http://www.ncip.info/introduction-to-ncip.html)).

#### Node.js

[Node.js](https://nodejs.org) is a JavaScript runtime for deploying
JavaScript code.

#### NPM

[npm](https://www.npmjs.com) is the Node.js Node Package Manager - a mechanism for distributing
packages of JavaScript code, used by Stripes.

#### OAS

The OpenAPI Specification ([OAS](https://en.wikipedia.org/wiki/OpenAPI_Specification)) for describing RESTful web services.
(Originally part of Swagger.)

#### Okapi gateway

See [Okapi](#okapi) explained above.

#### OLF

The [Open Library Foundation](https://www.openlibraryfoundation.org/)
is an independent not-for-profit organization to ensure the availability, accessibility and sustainability of open source and open access projects for and by libraries.
See [Newsroom](https://openlibraryfoundation.org/newsroom/).
OLF has joined the FOLIO community to help with the development of FOLIO.

#### OST
The [Officially Supported Technologies](https://wiki.folio.org/display/TC/Officially+Supported+Technologies) (OST) for each upcoming release (also known as Approved Technologies).

#### PC

The [FOLIO Product Council](https://wiki.folio.org/display/PC/)
and its [Charter](https://wiki.folio.org/display/PC/FOLIO+Product+Council+Charge)

#### PO

Each FOLIO Product Owner (PO) represents the business or user community, and is responsible for working with this group to determine what features will be in the product release.
Refer to the overview of [Product Owners](https://wiki.folio.org/display/PO/Product+Owners)
including explanation of "What is a Product Owner", getting involved and getting started,
and the [Directory of Product Owners by Area of Focus](https://wiki.folio.org/display/PO/Directory+of+Product+Owners+by+Area+of+Focus).

#### PostgreSQL

[PostgreSQL](https://www.postgresql.org/) (often called "Postgres") is
an open source enterprise-level relational database.

#### PoC

Proof-of-concept
([PoC](https://en.wikipedia.org/wiki/Proof_of_concept))

#### RAML

[RESTful API Modeling Language](https://raml.org) - a language for the
definition of HTTP-based APIs. Okapi module APIs (including the API of
Okapi itself) are [defined](/start/primer-raml/) in RAML files and JSON Schema files.

#### RDA

Resource Description and Access
([RDA](https://en.wikipedia.org/wiki/Resource_Description_and_Access)).

#### React

[React](https://facebook.github.io/react/)
is a JavaScript library for building user interfaces.

#### Redux
[Redux](https://redux.js.org) is a state container for
JavaScript. Stripes uses React and Redux for building stateful
JavaScript web applications.

#### Reference environments

Continuously built FOLIO systems to exhibit the state of development.
These are linked and their automation is explained at [Software build pipeline](/guides/automation/#software-build-pipeline).

#### REST

Representational State Transfer architectural style, and RESTful web services, enable interaction between systems using a well-known set of stateless operations and responses.

#### RFC

Request For Comments (RFCs).
Refer to the current [FOLIO RFC log](https://folio-org.atlassian.net/wiki/x/BADbF)
and the [RFC Process](https://wiki.folio.org/display/TC/RFC+Process).

(Refer to the previous set of [FOLIO RFCs](https://github.com/folio-org/rfcs) at folio-org GitHub.)

#### RMB

The [RAML Module Builder](https://github.com/folio-org/raml-module-builder) (RMB) framework, is a special FOLIO module that abstracts much functionality and enables the developer to focus on implementing business functions.

#### RMS

Release Management Stakeholders (RMS). Refer to the [Critical Service Patch Process](#csp) (CSP).

### Terms S-Z

#### SDLC

Software Development Life Cycle (SDLC)
[Software development process](https://en.wikipedia.org/wiki/Software_development_process).
Also abbreviated as DLC.

#### SEC

The [FOLIO Security Team](https://wiki.folio.org/display/SEC)
is the group is charged with overseeing the process related to identification and resolution of security vulnerabilities reported against FOLIO.

#### Slug

A human-readable identifier with keywords and alpha-numeric characters. Whitespace is replaced by a hyphen or an underscore character. Punctuation and accented characters are removed, thereby avoiding the need for special encoding.

Used for friendly URLs and reliable identifiers.

See Wikipedia [Slug](https://en.wikipedia.org/wiki/Clean_URL#Slug) and [etymology](https://en.wikipedia.org/wiki/Slug_(publishing)).

To "slugify" is to translate a string into a slug by replacing such characters.

#### Solr

[Apache Solr](https://en.wikipedia.org/wiki/Apache_Solr).

#### SPA

FOLIO is a single-page application ([SPA](https://en.wikipedia.org/wiki/Single-page_application)).

#### Spring

[Spring](https://spring.io/) is an application framework for the Java platform.

Some FOLIO modules are developed using the [folio-spring-base](https://github.com/folio-org/folio-spring-base) library and the Spring Way.

#### SRS

FOLIO Source Record Storage (SRS).

#### SRU

Search/Retrieve via URL
([SRU](https://loc.gov/standards/sru/)).
Version "[SRU 2.0](https://loc.gov/standards/sru/sru-2-0.html)"
is "searchRetrieve Version 1.0, OASIS Standard".

#### Stripes toolkit

See [Stripes](#stripes) and the various [Stripes entities](#stripes-entities) explained above.

#### SysOps

System operators, systems administrators of multi-user computer systems:
[Sysop](https://en.wikipedia.org/wiki/Sysop).

#### TC

The [FOLIO Technical Council](https://wiki.folio.org/display/TC/)
and its [Charter](https://wiki.folio.org/display/TC/Tech+Council+Charter).

The Wiki [Tree browser](https://wiki.folio.org/collector/pages.action?key=TC) helps to navigate the TC section of the Wiki.

#### TDO

[Technical Design Owners](/guidelines/development-design-review/#technical-design-owners-tdo).

#### TL

[Technical Lead](/guidelines/development-design-review/#technical-lead-tl).

#### UUID

Universally unique identifier, a 128-bit number, see
[UUID at Wikipedia](https://en.wikipedia.org/wiki/Universally_unique_identifier)
and [How to check for a valid UUID](/guides/uuids/).

#### UX

User experience ([UX](https://en.wikipedia.org/wiki/User_experience)).

See [User experience design](/guides/user-experience-design/)
and the [FOLIO UX](https://ux.folio.org/) documentation site.

#### Vert.x

[Vert.x](https://vertx.io) is a toolkit for building scalable, reactive
applications on the JVM. Vert.x is particularly suitable for
developing applications using the microservices architectural
pattern.

Some FOLIO modules are developed using the lightweight [folio-vertx-lib](https://github.com/folio-org/folio-vertx-lib) library.

#### WCAG

Web Content Accessibility Guidelines ([WCAG](https://en.wikipedia.org/wiki/Web_Content_Accessibility_Guidelines)).

#### Webpack

The Node.js module bundler, used to deploy Stripes modules.

#### WOLFcon

The World Open Library Foundation Conference ([WOLFcon](https://openlibraryfoundation.org/about/wolfcon/)).

#### WSAPI

A generic term for Web Services Application Programming Interface (see [API](#api) above).

#### Yarn

[Yarn](https://yarnpkg.com) is a package manager for Node.js and JavaScript.

#### ZooKeeper

[Apache ZooKeeper](https://zookeeper.apache.org/) is a service for highly reliable distributed coordination.  It has been used for Kafka coordination.

Kafka's KRaft mode replaces ZooKeeper, Kafka 4 doesn't support ZooKeeper.  Therefore ZooKeeper has been
[deprecated since Sunflower (R1-2025)](https://folio-org.atlassian.net/wiki/spaces/REL/pages/399081725/Sunflower+R1+2025+Required+manual+migrations)
and will be
[removed in Umbrellaleaf (2027)](https://folio-org.atlassian.net/wiki/spaces/TC/pages/966852629/Umbrellaleaf).

#### Z39.50

[Z39.50](https://en.wikipedia.org/wiki/Z39.50)
refers to ANSI/NISO standard Z39.50, and ISO standard 23950
"Information Retrieval (Z39.50): Application Service Definition and Protocol Specification".

The Library of Congress is the
[Z39.50 Maintenance Agency](https://loc.gov/z3950/agency/).

See [z2folio - the Z39.50-to-FOLIO gateway](https://github.com/folio-org/Net-Z3950-FOLIO).

<div class="folio-spacer-content"></div>

