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

Choose all names carefully, as there are various ramifications to later changing that.

In most cases (except when camelCase is required) use hyphenation to join words in a name, i.e. hyphen-separated strings (sometimes referred to as dash-separated).

The guide to [commence a new module](/guides/commence-a-module/) explains a typical directory layout and standard filenames.

## Module names

Each module has its own git repository.

Take care to choose wisely for the module/repository name. It will be disruptive to [change that](/guides/rename-module/).

Note that the repository name is normally the same as the module name.
The module name can be different, but that can lead to trouble.

Back-end modules do have a limit of 31 bytes for the module name,
and must be composed of only lowercase letters, digits, and hyphens.
Other restrictions for back-end module names are specified at the Wiki [Tenant ID and Module Name Restrictions](https://wiki.folio.org/display/DD/Tenant+Id+and+Module+Name+Restrictions).

The name uses the following scheme with a consistent prefix and hyphen-separated words:

* `mod-` prefix for [back-end modules](/source-code/map/#backend-mod) (e.g. mod-users, mod-inventory-storage).
* `edge-` prefix for [back-end modules](/source-code/map/#backend-edge) that connect to systems external to FOLIO (in particular, endpoints for standard protocols like NCIP)
* `stripes-` prefix for [Stripes modules](/source-code/map/#stripes) (e.g. stripes-core).
* `ui-` prefix for [front-end UI modules](/source-code/map/#ui) (e.g. ui-users).
* `ui-plugin-` prefix for [front-end UI plugin modules](/source-code/map/#ui-plugin) (e.g. ui-plugin-find-instance).
* `ui-handler-` prefix for [front-end UI handler modules](/source-code/map/#ui-handler) (e.g. ui-handler-stripes-registry) that consume, i.e. handle, events such as LOGIN and LOGOUT published by stripes-core.
* `folio-` prefix for [utility library modules](/source-code/map/#other) (e.g. folio-isbn-util).

Most module names will be in the plural sense, e.g. mod-notes, especially when responsible for collections of items.

Some back-end modules are paired. For example `mod-inventory` is the business logic module, while `mod-inventory-storage` is the associated storage module.
Having such a stem name, enables dividing a module into more layers.

The [version number](/guidelines/contributing/#version-numbers) of a module uses semantic versioning.

## Permissions

These are explained at [Permissions in Stripes and FOLIO](https://github.com/folio-org/stripes-core/blob/master/doc/permissions.md) (with some further links via this [FAQ](/faqs/explain-permissions-system/)).

FOLIO has a [Permissions naming convention](https://folio-org.atlassian.net/wiki/spaces/FOLIJET/pages/156368925/Permissions+naming+convention).

Permissions are defined in each module's ModuleDescriptor.

The naming scheme is a faceted dot-separated string, with the delimited terms as hyphen-separated words.
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

The name of an interface (its `id`) uses hyphen-separated strings.
It is normally the same as the set of `pathPattern`s for which it provides handlers.

Some examples:

* mod-inventory-storage provides various interfaces including `item-storage` and `loan-types` and others.

The [version number](/guidelines/contributing/#version-numbers) of an interface uses the first two portions of semantic versioning.
There does not need to be any correlation between the module version and the version of the interfaces it implements.

The back-end modules can also provide
[system interfaces](https://github.com/folio-org/okapi/blob/master/doc/guide.md#system-interfaces).
These Okapi interface names start with underscore, e.g. the Tenant Interface `_tenant`

## API endpoints

The back-end modules define their routes and API endpoints in their [API descriptions](/reference/api/),
and declare the endpoints as the pathPatterns in the interfaces defined by their ModuleDescriptor.

Endpoints use hyphen-separated strings, with URI parameters as camelCase.
There is no trailing slash.

Some examples:

* mod-inventory-storage declares `/contributor-name-types/{contributorNameTypeId}`

All backend modules are required to provide the [module health check](https://wiki.folio.org/display/DD/Back+End+Module+Health+Check+Protocol) `/admin/health` endpoint.

The special prefix `/_` is used to to distinguish the routing for the core endpoints of
[Okapi internal web services](https://github.com/folio-org/okapi/blob/master/doc/guide.md#okapis-own-web-services)
from the extension points provided by modules (e.g. `/_/proxy`).

## Release branches and tags

Each release is tagged in git, with a name beginning with `v` and followed by the version number (e.g. `v2.3.5`).

There are long-lived release branches, with a name beginning with `b` and followed by the major and minor version number (e.g. `b2.17`).

See further information for
[front-end](https://github.com/folio-org/stripes/blob/master/doc/release-procedure.md#version-numbers-branches-and-tags)
and
[back-end](/guidelines/release-procedures/#bug-fix-releases)
modules.

