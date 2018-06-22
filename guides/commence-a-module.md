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

See also the guidelines to [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/), as well as the [Getting started](/start/) fundamental documentation and primers.

The essential directories and files are explained below for [back-end](#back-end-modules) and [front-end](#front-end-modules) modules.
Of course any module might need extras.

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

The `descriptors` directory holds the template Descriptor files. For a Maven-based system, the pom.xml will have tasks to replace tokens with this module's `artifactId` and `version` to generate the descriptors into the `target` directory.

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

## Structure {#front-end-structure}

This is a typical directory layout, excluding the general boilerplate files and the usual JavaScript and CSS files:

```
├── Jenkinsfile
├── data
│   ├── various
├── icons
│   ├── app.png
│   └── app.svg
├── lib
│   ├── various
├── package.json
├── settings
│   ├── various
├── sound
│   ├── checkout_error.m4a
│   └── checkout_success.m4a
├── test
│   └── ui-testing
├── translations
    └── ui-users
        ├── de.json
        ├── en.json
        └── hu.json
```

## Jenkinsfile {#front-end-jenkinsfile}

The `Jenkinsfile` declares specific build steps for the continuous integration process.

## package.json {#front-end-packagejson}

See the "[Stripes application metadata bundles](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md)"
document which explains the specification for standard and extension fields.

## Descriptors {#frontend-end-descriptors}

The Stripes Core will generate the ModuleDescriptor.json for this UI module from its package.json file.

## Data {#front-end-data}

The optional `data` directory holds data specific to this app.

## Icons {#front-end-icons}

The `icons` directory holds icon files specific to this app.
Some icons are provided by Stripes itself.

See the [Icons](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md#icons)
section of the "Stripes application metadata bundles" document.

## Lib {#front-end-lib}

The `lib` directory holds local libraries specific to this app.

## Settings {#front-end-Settings}

The `settings` directory holds settings specific to this app.

## Sound {#front-end-Sound}

The optional `sound` directory holds sound files specific to this app.

## Test {#front-end-test}

The `test` directory holds the ui-testing facilities specific to this app.

See the [ui-testing](https://github.com/folio-org/ui-testing) documentation.

## Translations {#front-end-translations}

The `translations` directory holds the locale data for this app.
The various `stripes-components` are separately handled.

See the "[I18n best practices](https://github.com/folio-org/stripes-core/blob/master/doc/i18n.md)" document, and facilities provided by Stripes Core.


