---
layout: page
title: Commence a module - structure and configuration
permalink: /guides/commence-a-module/
menuInclude: no
menuTopTitle: Guides
---

This guide explains how to commence a new module, including its structure, directory layout, configuration for continuous integration, sample data, etc.

# Introduction

Using consistent structure and configuration will assist the development.
All developers can know what to expect.
The continuous integration and deployment will be easier to establish and be reliable.

See also the guidelines to [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/).

Of course any module might need extra directories and files, but the following are the essential ones.

# General

All modules will have the normal boilerplate files such as README.md, LICENSE, CONTRIBUTING.md, etc.

# Back-end modules

Server-side modules include all those named `mod-*`.
Follow the [mod-notes](https://github.com/folio-org/mod-notes) as an example.

The `NEWS.md` lists the main changes for each release. Follow the layout of other back-end modules.

## Structure {#back-end-structure}

This is a typical directory layout, excluding the general boilerplate files and build system files (e.g. `pom.xml` and `target` for Maven-based modules):

```
├── Dockerfile
├── Jenkinsfile
├── descriptors
│   ├── DeploymentDescriptor-template.json
│   └── ModuleDescriptor-template.json
├── doc
│   ├── index.md
│   └── guide.md
├── docker
│   └── docker-entrypoint.sh
├── ramls
│   └── raml-util
├── reference-data
│   └── vendor-categories
├── sample-data
│   └── vendors
├── src
```

## Docker {#back-end-docker}

The `Dockerfile` and `docker` directory with its `docker-entrypoint.sh` file.

## Jenkinsfile {#back-end-jenkinsfile}

The `Jenkinsfile` declares specific build steps for the continuous integration process.

## Descriptors {#back-end-descriptors}

The `descriptors` directory holds the template Descriptor files. For a Maven-based system, the pom.xml will have tasks to replace tokens with this module's `artifactId` and `version` and produce the descriptors into the `target` directory.

## Documentation {#back-end-doc}

The `doc` directory holds additional documentation beyond the standard top-level README.md file.
Usually in Markdown format.

## RAMLs {#back-end-ramls}

The `ramls` directory holds the RAML and Schema and examples files specific to this module.
Normally there will also be the `ramls/raml-util` shared files as a git submodule of the [raml](https://github.com/folio-org/raml) repository.
Some modules only have a `raml-util` because their files are all located in the shared space.

## Reference data {#back-end-reference-data}

The optional `reference-data` directory can hold data required for [sample data](#back-end-sample-data) to refer to.
For example, if the vendors in your sample data refer to vendor categories by UUID, the vendor categories (with their UUIDs) could be defined in the `reference-data/vendor-categories` directory, in the format expected by the module's relevant endpoint for POSTing the data.
This makes it easy to write a script to load the reference data using the module's web service API.

## Sample data {#back-end-sample-data}

The `sample-data` directory holds sample data specific for this module.
It should be in the format expected by the module's relevant endpoint for POSTing the data.
This makes it easy to write a script to load the sample data using the module's web service API.

If the sample data refers to [reference data](#back-end-reference-data), those data can be defined in the `reference-data` directory.

# Front-end modules

Client-side modules include all those named `stripes-*` and `ui-*`.
Follow the [ui-users](https://github.com/folio-org/ui-users) as an example.

The [stripes-cli](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md#app-development) will generate an initial skeleton UI app module structure named with the `ui-` prefix.

The `CHANGELOG.md` lists the main changes for each release. Follow the layout of other front-end modules.

TODO: Add the typical structure.

