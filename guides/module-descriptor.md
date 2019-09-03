---
layout: page
title: ModuleDescriptor
permalink: /guides/module-descriptor/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

This guide provides an overview of the ModuleDescriptor.

The ModuleDescriptor is introduced in the Okapi Guide
(e.g. [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#what-are-modules)
and [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#example-4-complete-moduledescriptor)).

The MD adheres to the [ModuleDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) schema.

## Maintenance

### Back-end modules

For back-end modules, a template is maintained.
This is usually at `./descriptors/ModuleDescriptor-template.json` and is transformed by the module's build process into the `target/ModuleDescriptor.json` file.
See example at [mod-notes](https://github.com/folio-org/mod-notes/blob/master/descriptors/ModuleDescriptor-template.json).

### Front-end modules

For front-end UI modules, the `ModuleDescriptor.json` is generated from various information maintained in the `package.json` file.
See example at [ui-users](https://github.com/folio-org/ui-users/blob/master/package.json).

## Registry

As part of the continuous integration process, each ModuleDescriptor.json is published to the FOLIO Registry at `https://folio-registry.aws.indexdata.com/`

## MD properties

```
TODO: Provide brief explanations of each main section.
```

The "metadata" section provides some additional items.
These are used to assist the generation of a documentation snippet for Docker Hub,
and to configure folio-ansible.
Currently only two items:

* `containerMemory` -- A hint about the minimum amount of memory required to run this module.
The values correlate with that used by [folio-ansible](https://github.com/folio-org/folio-ansible/tree/master/group_vars) for the [reference environments](/guides/automation/#reference-environments).
Note that these installations have a small amount of data and low activity load.

* `databaseConnection` -- Whether this module utilises a database.

