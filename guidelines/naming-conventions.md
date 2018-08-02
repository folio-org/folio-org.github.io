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

## Module names

Each module has its own git repository. The name uses the following scheme with a consistent prefix and dash-separated words:

* `mod-` prefix for back-end modules (e.g. mod-users, mod-inventory-storage).
* `ui-` prefix for front-end UI modules (e.g. ui-users).
* `stripes-` prefix for Stripes modules (e.g. stripes-core).

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

## API endpoints

Endpoints use dash-separated strings, with URI parameters as camelCase.

Some examples:

* mod-inventory-storage declares `/contributor-name-types/{contributorNameTypeId}`

