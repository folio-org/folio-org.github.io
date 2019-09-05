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

For back-end modules, a template is [maintained](/guides/commence-a-module/#back-end-descriptors).
This is usually at `./descriptors/ModuleDescriptor-template.json` and is transformed by the module's build process into the `target/ModuleDescriptor.json` file.
See example at [mod-notes](https://github.com/folio-org/mod-notes/blob/master/descriptors/ModuleDescriptor-template.json).

To validate changes, utilise a JSON Schema validator such as [z-schema](https://github.com/zaggino/z-schema):

```
cd mod-notes
jq '.' descriptors/ModuleDescriptor-template.json
z-schema --pedanticCheck \
  ../okapi/okapi-core/src/main/raml/ModuleDescriptor.json \
  ./descriptors/ModuleDescriptor-template.json
```

### Front-end modules

For front-end UI modules, the `ModuleDescriptor.json` is generated from various information
that is [maintained](/guides/commence-a-module/#frontend-end-descriptors) in the `package.json` file.
See example at [ui-users](https://github.com/folio-org/ui-users/blob/master/package.json).

To validate changes, first use [stripes-cli](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md) to generate the MD.
Then utilise a JSON Schema validator such as [z-schema](https://github.com/zaggino/z-schema):

```
cd ui-users
jq '.' package.json
stripes mod descriptor --full --output /tmp
z-schema --pedanticCheck \
  ../okapi/okapi-core/src/main/raml/ModuleDescriptor.json \
  /tmp/users.json
```

## Registry

As part of the continuous integration process, each ModuleDescriptor.json is published to the FOLIO Registry at `https://folio-registry.aws.indexdata.com/`

## ModuleDescriptor properties

### Introduction {#md-introduction}

Refer to the general [introduction](#introduction) above.

### General MD properties

Each main property is briefly described in the
[ModuleDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) schema.

The following sub-sections explain some properties in more detail ...

```
TODO: Provide brief explanations of some sections.
```

### metadata

The "metadata" section enables some additional items.
The MD schema enables any JSON object.

**NOTE:** 20190901: The following items are currently used to assist the generation of a documentation snippet for Docker Hub.
These will soon be replaced with information from the new LaunchDescriptor.

Currently only two items are used:

* `containerMemory` -- A hint about the minimum amount of memory required to run this module.
The values correlate with that used by [folio-ansible](https://github.com/folio-org/folio-ansible/tree/master/group_vars) for the FOLIO [reference environments](/guides/automation/#reference-environments).
Note that these installations have a small amount of data and low activity load.

* `databaseConnection` -- Whether this module utilises a database.

## LaunchDescriptor properties

### Introduction {#ld-introduction}

The LaunchDescriptor is introduced in the Okapi Guide
(e.g. at sections [Deployment and Discovery](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment-and-discovery)
and [Deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment)
and [Auto-deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#auto-deployment)).

The LD adheres to the [LaunchDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/LaunchDescriptor.json) schema.

As explained in the Okapi Guide, the LaunchDescriptor can be a separate descriptor, or be part of the ModuleDescriptor.
The LaunchDescriptor can utilise various methods for [deployment](https://github.com/folio-org/okapi/blob/master/doc/guide.md#deployment).

For the suite of [back-end modules](/source-code/#server-side) that are hosted at folio-org, each one has a LaunchDescriptor for Docker, and the LD is included in the module's ModuleDescriptor file.
This enables ready default deployment.

The properties correlate with that used by [folio-ansible](https://github.com/folio-org/folio-ansible/tree/master/group_vars) for the FOLIO [reference environments](/guides/automation/#reference-environments).
Note that these installations have a small amount of data and low activity load.

### General LD properties

Each main property is briefly described in the
[LaunchDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/LaunchDescriptor.json) schema.

The following sub-sections explain some properties in more detail ...

```
TODO: Provide brief explanations of some sections.
```

