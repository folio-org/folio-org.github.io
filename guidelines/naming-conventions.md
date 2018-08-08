---
layout: page
title: Naming conventions
permalink: /guidelines/naming-conventions/
menuInclude: no
menuTopTitle: Guidelines
---

This document declares the naming conventions, which enable consistency.

## Introduction

Note that some early modules did not follow some aspects of these naming schemes.

Choose names carefully, as there are various ramifications to later changing that.

## Module names

Each module has its own git repository. The name uses the following scheme with a consistent prefix and dash-separated words:

* `mod-` prefix for back-end modules (e.g. mod-users, mod-inventory-storage).
* `ui-` prefix for front-end UI modules (e.g. ui-users).
* `stripes-` prefix for Stripes modules (e.g. stripes-core).

Some back-end modules are paired. For example `mod-inventory` is the business logic module, while `mod-inventory-storage` is the associated storage module.

## Permissions

These are explained at [Permissions in Stripes and FOLIO](https://github.com/folio-org/stripes-core/blob/master/doc/permissions.md) (with some further links via this [FAQ](/faqs/explain-permissions-system/)).

Permissions are defined in each module's ModuleDescriptor.

The naming scheme is a faceted dot-separated string, with the delimited terms as dash-separated words.
The first portion is the exact name of the responsible module (back-end modules drop the `mod-` prefix).

Some examples:

* mod-users declares `users.collection.get`
* mod-inventory-storage declares `inventory-storage.loan-types.collection.get`
* ui-users declares `ui-users.view`

## Schema

JSON key names use camelCase.

Some examples:

* mod-inventory-storage defines `contributorNameTypes`
* All modules use `totalRecords` and `id` and `metadata`

## Interfaces

The back-end modules define each
[interface](https://github.com/folio-org/okapi/blob/master/doc/guide.md#architecture)
that they provide, in their ModuleDescriptor.
Each module can define more than one interface.
Normally an interface is defined by only one module, but Okapi does allow different modules to provide the same interface by using
[multiple interfaces](https://github.com/folio-org/okapi/blob/master/doc/guide.md#multiple-interfaces).

The name of an interface (its `id`) uses dash-separated strings.
It is normally the same as the set of `pathPattern`s for which it provides handlers.

Some examples:

* mod-inventory-storage provides various interfaces including `item-storage` and `loan-types` and others.

The [version number](/guidelines/contributing/#version-numbers) of an interface uses the first two portions of semantic versioning.
There does not need to be any correlation between the module version and the version of the interfaces it implements.

The back-end modules can also provide
[system interfaces](https://github.com/folio-org/okapi/blob/master/doc/guide.md#system-interfaces).
These Okapi interface names start with underscore, e.g. the Tenant Interface `_tenant`

## API endpoints

The back-end modules define their routes and API endpoints in their [RAML files](/reference/api/),
and declare the endpoints as the pathPatterns in the interfaces defined by their ModuleDescriptor.

Endpoints use dash-separated strings, with URI parameters as camelCase.
There is no trailing slash.

Some examples:

* mod-inventory-storage declares `/contributor-name-types/{contributorNameTypeId}`

The special prefix `/_` is used to to distinguish the routing for the core endpoints of
[Okapi internal web services](https://github.com/folio-org/okapi/blob/master/doc/guide.md#okapis-own-web-services)
from the extension points provided by modules, e.g. `/_/proxy`

