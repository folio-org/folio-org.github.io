---
layout: page
title: Commence a module - structure and configuration
permalink: /guides/commence-a-module/
menuInclude: no
menuTopTitle: Guides
---

This guide explains how to commence a new module, including its structure, directory layout, configuration for continuous integration, sample data, etc.

## Introduction

Using consistent structure and configuration will assist the development.
All developers can know what to expect.
The continuous integration and deployment will be easier to establish and be reliable.

See also the guidelines to [Create a new FOLIO module and do initial setup](/guidelines/create-new-repo/).

Be familiar with the [Getting started](/start/) fundamental documentation and primers.

The essential directories and files are explained below for [back-end](#back-end-modules) and [front-end](#front-end-modules) modules.
Of course any module might need extras.

## General

All modules will have the [normal boilerplate files](/guidelines/create-new-repo/) such as README.md, LICENSE, CONTRIBUTING.md, etc.

The [Naming conventions](/guidelines/naming-conventions/) guidelines apply.

Module documentation is kept with the relevant repository, while broad and project-wide documentation is here at the dev.folio.org site.

## Back-end modules

Server-side modules include all those named `mod-*`.
Follow the structure and files of [mod-notes](https://github.com/folio-org/mod-notes) as an example.

The [mod-rmb-template](https://github.com/folio-org/mod-rmb-template)
provides a Maven archetype to commence a new RMB-based module.

The `NEWS.md` lists the main changes for each release. Follow how the other back-end modules use this file.

### Structure {#back-end-structure}

This is a typical directory layout, excluding the general boilerplate files and build system files (e.g. `pom.xml` and `target` for Maven-based modules):

```
├── Dockerfile
├── Jenkinsfile
├── descriptors/
│   ├── DeploymentDescriptor-template.json
│   └── ModuleDescriptor-template.json
├── doc/
│   ├── various.md
├── ramls/
│   ├── various-schema.json
│   └── raml-util/
├── reference-data/
│   └── instance-types/
│   └── loan-types/
│   └── .../
├── sample-data/
│   └── instances/
│   └── items/
│   └── .../
├── src/
```

### Dockerfile {#back-end-dockerfile}

The `Dockerfile`. See [explanation](/guides/module-descriptor/#dockerfile).

### Jenkinsfile {#back-end-jenkinsfile}

The `Jenkinsfile` declares specific build steps for the continuous integration [process](/guides/automation/#jenkins).
See [explanation](/guides/jenkinsfile/).

### Descriptors {#back-end-descriptors}

The `descriptors` directory holds the template Descriptor files. For a Maven-based system, the pom.xml will have tasks to replace tokens with this module's `artifactId` and `version` to generate the descriptors into the `target` directory.
See example at [mod-notes/pom.xml](https://github.com/folio-org/mod-notes/blob/master/pom.xml) and the 'filter-descriptor-inputs' and 'rename-descriptor-outputs' tasks.

Note that Spring-based modules use replacement tokens of the form `"@artifactId@-@version@"` instead of the normal `"${artifactId}-${version}"`.

Refer to explanation of [ModuleDescriptors](/guides/module-descriptor/) and default [LaunchDescriptors](/guides/module-descriptor/#launchdescriptor-properties).

### Documentation {#back-end-doc}

The optional `docs` (or `doc`) directory holds additional documentation beyond the standard top-level README.md file.
Usually in Markdown format.

Consider the guide to [increase visibility of module documentation](/guides/visibility-module-docs/).

### API descriptions

Back-end repositories will provide API descriptions. These will either be RAML or OpenAPI (OAS).

The reference [API documentation](/reference/api/) is generated from these files. Provide a clear "description" field for each endpoint.

Set the Jenkinsfile [configuration](/guides/jenkinsfile/) `doApiLint` parameter
and `doApiDoc` parameter, to enable these during continuous integration.

#### RAMLs {#back-end-ramls}

The top-level `ramls` directory holds the RAML and Schema and examples files specific to this module.
Normally there will also be the [git submodule](https://git-scm.com/docs/git-submodule) at `ramls/raml-util` being the shared files of the [raml](https://github.com/folio-org/raml) repository.

Some modules only have a `ramls/raml-util` and not other files, because their files are all located in that shared space.

Configure the CI jobs `doApiLint` and `doApiDoc` as explained above.

See the [Primer for RAML and JSON Schema](/start/primer-raml/).

#### OpenAPI (OAS) {#back-end-oas}

The relevant `openapi` directory (e.g. "`src/main/resources/openapi`" or "`src/main/resources/swagger.api`" etc.) holds the API description OAS and Schema and examples files specific to this module.

Configure the CI jobs `doApiLint` and `doApiDoc` as explained above.

See the [Primer for OpenAPI (OAS) and JSON Schema](/start/primer-oas/).

#### API schema {#back-end-api-schema}

The [API descriptions](#api-descriptions) will refer to their related schema files.

The reference [API documentation](/reference/api/) is generated from these files.

For each of the schema properties, as early as possible [provide](/guides/describe-schema/) a clear description and define the constraints.

Take care with linking to schema files:
In our schemas, the value of "$ref" in the parent schema is a relative pathname to the child schema.
In the RAML files, the "type" is declared as a symbolic name for use elsewhere in the RAML file
(its declared value is the path to the schema, relative to that RAML file).

### Database schema {#back-end-database-schema}

For RMB-based modules the DB schema defines this module's tables, indexes, joins, etc.
It is located at `src/main/resources/templates/db_scripts/schema.json`

When SQL scripts are necessary, they are also stored in that `db_scripts` directory.

See further information in the "[Tenant API](https://github.com/folio-org/raml-module-builder#tenant-api)" section of the RMB README document.

### Reference data {#back-end-reference-data}

The optional `reference-data` directory can hold data required for [sample data](#back-end-sample-data) to refer to.
For example, if the vendors in your sample data refer to vendor categories by UUID, the vendor categories (with their UUIDs) could be defined in the `reference-data/vendor-categories` directory, in the format expected by the module's relevant endpoint for POSTing the data.

Loading reference-data and sample-data is achieved during the tenant initialisation phase.
Refer to the "[Tenant API](https://github.com/folio-org/raml-module-builder#tenant-api)" section of the RMB README document.
Refer to the "[Tenant Interface](https://github.com/folio-org/okapi/blob/master/doc/guide.md#tenant-interface)"
and "[Tenant Parameters](https://github.com/folio-org/okapi/blob/master/doc/guide.md#tenant-parameters)"
and "[Install modules per tenant](https://github.com/folio-org/okapi/blob/master/doc/guide.md#install-modules-per-tenant)"
sections of the Okapi Guide.

For example:
```
... proxy/tenants/diku/install ... tenantParameters=loadSample%3Dtrue%2CloadReference%3Dtrue
```

### Sample data {#back-end-sample-data}

The `sample-data` directory holds sample data specific for this module.
It should be in the format expected by the module's relevant endpoint for POSTing the data.

If the sample data refers to [reference data](#back-end-reference-data), those data can be defined in the `reference-data` directory.

See example data at [mod-inventory-storage](https://github.com/folio-org/mod-inventory-storage).

## Front-end modules

Client-side modules include all those named `stripes-*` and `ui-*`.
Follow the structure and files of [ui-users](https://github.com/folio-org/ui-users) as an example.

The [stripes-cli](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md#app-development) will generate an initial skeleton UI app module structure named with the `ui-` prefix.

[The Stripes Module Developer's Guide](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md) explains what is expected of a UI module.

The `CHANGELOG.md` lists the main changes for each release. Follow how the other front-end modules use this file.

### Structure {#front-end-structure}

This is a typical directory layout, excluding the general boilerplate files and the usual JavaScript and CSS files:

```
├── Jenkinsfile
├── data/
│   ├── various
├── doc/
│   ├── various.md
├── icons/
│   ├── app.png
│   └── app.svg
├── lib/
│   ├── various
├── package.json
├── sound/
│   ├── checkout_error.m4a
│   └── checkout_success.m4a
├── src/
│   ├── various js and css files
│   └── settings/
├── test/
│   └── ui-testing/
├── translations/
    └── ui-users/
        ├── en.json
```

### Jenkinsfile {#front-end-jenkinsfile}

The `Jenkinsfile` declares specific build steps for the continuous integration [process](/guides/automation/#jenkins).
See [explanation](/guides/jenkinsfile).

### package.json {#front-end-packagejson}

See the "[Stripes application metadata bundles](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md)"
document which explains the specification for standard and extension fields.

The "Modules" section of the [The Stripes Module Developer's Guide](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md#modules) explains the `stripes` section of the configuration, including the `pluginType`, the `route` to address this module, the `okapiInterfaces` for any back-end module dependencies, and the optional `permissionsets`.
The [Explain the FOLIO permissions system](/faqs/explain-permissions-system/) FAQ will assist.

### Descriptors {#frontend-end-descriptors}

The Stripes Core will generate the ModuleDescriptor.json for this UI module from its package.json file.

Refer to explanation of [ModuleDescriptors](/guides/module-descriptor/).

### Data {#front-end-data}

The optional `data` directory holds data specific to this app.

### Documentation {#front-end-doc}

The optional `doc` (or `docs`) directory holds additional documentation beyond the standard top-level README.md file.
Usually in Markdown format.

Consider the guide to [increase visibility of module documentation](/guides/visibility-module-docs/).

### Icons {#front-end-icons}

The optional `icons` directory holds icon files specific to this app.
Some icons are provided by Stripes itself.

See the [Icons](https://github.com/folio-org/stripes-core/blob/master/doc/app-metadata.md#icons)
section of the "Stripes application metadata bundles" document.

### Lib {#front-end-lib}

The optional `lib` directory holds local libraries specific to this app.

Some modules just have all of their code in the top-level directory.

### Settings {#front-end-Settings}

The `src/settings` directory holds settings specific to this app.

### Sound {#front-end-Sound}

The optional `sound` directory holds sound files specific to this app.

### src {#front-end-src}

The source files for this module.

### Test {#front-end-test}

The `test` directory holds the UI testing facilities specific to this app.

Refer to [How to run tests prior to commit](/faqs/how-to-test-prior-to-commit/) for brief explanation and links to testing facilities.

### Translations {#front-end-translations}

The `translations` directory holds the locale data for this app.
As shown in the example listing, the files are within a sub-directory with the same name as the git repository of this module.

The various `stripes-components` are separately handled.

See the "[i18n best practices](https://github.com/folio-org/stripes/blob/master/doc/i18n.md)" internationalization and localization documentation, and facilities provided by Stripes Core.

As explained there, the `en.json` file provides the default keys and strings.
There is no need for other placeholder files.
The files for other languages are automatically generated and merged by Lokalise, with the assistance of human translators.

<div class="folio-spacer-content"></div>

