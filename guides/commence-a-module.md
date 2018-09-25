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

Be familiar with the [Getting started](/start/) fundamental documentation and primers.

The essential directories and files are explained below for [back-end](#back-end-modules) and [front-end](#front-end-modules) modules.
Of course any module might need extras.

# General

All modules will have the [normal boilerplate files](/guidelines/create-new-repo/) such as README.md, LICENSE, CONTRIBUTING.md, etc.

The [Naming conventions](/guidelines/naming-conventions/) guidelines apply.

Module documentation is kept with the relevant repository, while broad and project-wide documentation is here at the dev.folio.org site.

# Back-end modules

Server-side modules include all those named `mod-*`.
Follow the structure and files of [mod-notes](https://github.com/folio-org/mod-notes) as an example.

The `NEWS.md` lists the main changes for each release. Follow how the other back-end modules use this file.

## Structure {#back-end-structure}

This is a typical directory layout, excluding the general boilerplate files and build system files (e.g. `pom.xml` and `target` for Maven-based modules):

```
├── Dockerfile
├── Jenkinsfile
├── descriptors
│   ├── DeploymentDescriptor-template.json
│   └── ModuleDescriptor-template.json
├── doc
│   ├── various.md
├── ramls
│   └── raml-util
├── reference-data
│   └── instance-types
│   └── loan-types
│   └── ...
├── sample-data
│   └── instances
│   └── items
│   └── ...
├── src
```

## Dockerfile {#back-end-dockerfile}

The `Dockerfile`.

## Jenkinsfile {#back-end-jenkinsfile}

The `Jenkinsfile` declares specific build steps for the continuous integration [process](/guides/automation/#jenkins).
See [explanation](/guides/jenkinsfile/).

## Descriptors {#back-end-descriptors}

The `descriptors` directory holds the template Descriptor files. For a Maven-based system, the pom.xml will have tasks to replace tokens with this module's `artifactId` and `version` to generate the descriptors into the `target` directory.
See example at [mod-notes/pom.xml](https://github.com/folio-org/mod-notes/blob/master/pom.xml) and the 'filter-descriptor-inputs' and 'rename-descriptor-outputs' tasks.

## Documentation {#back-end-doc}

The optional `doc` directory holds additional documentation beyond the standard top-level README.md file.
Usually in Markdown format.

## RAMLs {#back-end-ramls}

The `ramls` directory holds the RAML and Schema and examples files specific to this module.
Normally there will also be the `ramls/raml-util` shared files as a git submodule of the [raml](https://github.com/folio-org/raml) repository.
Some modules only have a `raml-util` because their files are all located in the shared space.

Add an entry to the API docs [configuration](/faqs/how-to-configure-api-doc-generation/).
Then set the Jenkinsfile [configuration](/guides/jenkinsfile/) `publishAPI` parameter
and `runLintRamlCop` parameter, to enable these during continuous integration.

The reference [API documentation](/reference/api/) is generated from these files. Provide a clear "description" field for each endpoint.

See the [Primer for RAML and JSON Schema](/start/primer-raml/).

## API schema {#back-end-api-schema}

The `ramls` directory holds the related schema files.

The reference [API documentation](/reference/api/) is generated from these files.
[Provide](/guides/describe-schema/) a clear "description" field for each of the schema properties.

## Database schema {#back-end-database-schema}

The DB schema defines this module's tables, indexes, joins, etc.
It is located at `src/main/resources/templates/db_scripts/schema.json`

When SQL scripts are necessary, they are also stored in that `db_scripts` directory.

## Reference data {#back-end-reference-data}

The optional `reference-data` directory can hold data required for [sample data](#back-end-sample-data) to refer to.
For example, if the vendors in your sample data refer to vendor categories by UUID, the vendor categories (with their UUIDs) could be defined in the `reference-data/vendor-categories` directory, in the format expected by the module's relevant endpoint for POSTing the data.
This makes it easy to write a script to load the reference data using the module's web service API.

## Sample data {#back-end-sample-data}

The `sample-data` directory holds sample data specific for this module.
It should be in the format expected by the module's relevant endpoint for POSTing the data.
This makes it easy to write a script to load the sample data using the module's web service API.

If the sample data refers to [reference data](#back-end-reference-data), those data can be defined in the `reference-data` directory.

See example data at [mod-inventory-storage](https://github.com/folio-org/mod-inventory-storage).

# Front-end modules

Client-side modules include all those named `stripes-*` and `ui-*`.
Follow the structure and files of [ui-users](https://github.com/folio-org/ui-users) as an example.

The [stripes-cli](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md#app-development) will generate an initial skeleton UI app module structure named with the `ui-` prefix.

[The Stripes Module Developer's Guide](https://github.com/folio-org/stripes-core/blob/master/doc/dev-guide.md) explains what is expected of a UI module.

The `CHANGELOG.md` lists the main changes for each release. Follow how the other front-end modules use this file.

## Structure {#front-end-structure}

This is a typical directory layout, excluding the general boilerplate files and the usual JavaScript and CSS files:

```
├── Jenkinsfile
├── data
│   ├── various
├── doc
│   ├── various.md
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

The `Jenkinsfile` declares specific build steps for the continuous integration [process](/guides/automation/#jenkins).
See [explanation](/guides/jenkinsfile).

## package.json {#front-end-packagejson}

See the "[Stripes application metadata bundles](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md)"
document which explains the specification for standard and extension fields.

The "Modules" section of the [The Stripes Module Developer's Guide](https://github.com/folio-org/stripes-core/blob/master/doc/dev-guide.md#modules) explains the `stripes` section of the configuration, including the `pluginType`, the `route` to address this module, the `okapiInterfaces` for any back-end module dependencies, and the optional `permissionsets`.
The [Explain the FOLIO permissions system](/faqs/explain-permissions-system/) FAQ will assist.

## Descriptors {#frontend-end-descriptors}

The Stripes Core will generate the ModuleDescriptor.json for this UI module from its package.json file.

## Data {#front-end-data}

The optional `data` directory holds data specific to this app.

## Documentation {#front-end-doc}

The optional `doc` directory holds additional documentation beyond the standard top-level README.md file.
Usually in Markdown format.

## Icons {#front-end-icons}

The optional `icons` directory holds icon files specific to this app.
Some icons are provided by Stripes itself.

See the [Icons](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md#icons)
section of the "Stripes application metadata bundles" document.

## Lib {#front-end-lib}

The optional `lib` directory holds local libraries specific to this app.

Some modules just have all of their code in the top-level directory.

## Settings {#front-end-Settings}

The `settings` directory holds settings specific to this app.

## Sound {#front-end-Sound}

The optional `sound` directory holds sound files specific to this app.

## Test {#front-end-test}

The `test` directory holds the ui-testing facilities specific to this app.

See the [ui-testing](https://github.com/folio-org/ui-testing) documentation.

## Translations {#front-end-translations}

The `translations` directory holds the locale data for this app.
As shown in the example listing, the files are within a sub-directory with the same name as the git repository of this module.

The various `stripes-components` are separately handled.

See the "[I18n best practices](https://github.com/folio-org/stripes-core/blob/master/doc/i18n.md)" internationalization documentation, and facilities provided by Stripes Core.


