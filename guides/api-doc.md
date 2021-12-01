---
layout: page
title: Generate API documentation
permalink: /guides/api-doc/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

For server-side projects that utilise RAML or OpenAPI (OAS), use the tool `api-doc` to generate API documentation from its API description files and schema and examples.

The tool is available for use during FOLIO Continuous Integration builds, and also for local use prior to commit.

This tool replaces the deprecated "generate-api-docs" (publishAPI) facility.

## Usage

For use during FOLIO CI builds, refer to the Jenkinsfile [configuration](#jenkinsfile) below.

For local use, clone the "[folio-tools](https://github.com/folio-org/folio-tools)" repository parallel to clones of back-end project repositories, and use its [api-doc](https://github.com/folio-org/folio-tools/tree/master/api-doc) facility.
Refer to that document for local installation instructions.

### Python

The Python script will search the configured directories to find relevant API description files, and will process each file to generate the API documentation representation.

<a id="properties"></a>Where the main options are:

* `-t,--types` -- The type of API description files to search for.
  Required. Space-separated list.
  One or more of: `RAML OAS`
* `-d,--directories` -- The list of directories to be searched.
  Required. Space-separated list.
* `-e,--excludes` -- List of additional sub-directories and files to be excluded.
  Optional. Space-separated list.
  By default it excludes certain well-known directories (such as `raml-util`).
  Use the option `--loglevel debug` to report what is being excluded.

See help for the full list (including the default output directory):

```
python3 ../folio-tools/api-doc/api_doc.py --help
```

Example for RAML:

```
cd $GH_FOLIO/mod-courses
python3 ../folio-tools/api-doc/api_doc.py \
  -t RAML \
  -d ramls
```

Example for OAS:

```
cd $GH_FOLIO/mod-eusage-reports
python3 ../folio-tools/api-doc/api_doc.py \
  -t OAS \
  -d src/main/resources/openapi \
  -e headers
```

Example for both RAML and OpenAPI (OAS), i.e. when preparing for transition:

```
cd $GH_FOLIO/mod-foo
python3 ../folio-tools/api-doc/api_doc.py \
  -t RAML OAS \
  -d ramls src/main/resources/oas
```

### Jenkinsfile

To use "api-doc" with FOLIO Continuous Integration, add the following configuration to the project's [Jenkinsfile](/guides/jenkinsfile/).

Note that the project should also use "[api-lint](/guides/api-lint/)" which utilises the same configuration for the [properties](#properties) apiTypes, apiDirectories, etc.)
Also see [upgrade notes](/guides/api-lint/#jenkinsfile-for-raml) there.

#### Jenkinsfile for RAML

```
buildMvn {
...
  doApiDoc = true
  doApiLint = true
  apiTypes = 'RAML' // Required. Space-separated list: RAML OAS
  apiDirectories = 'ramls' // Required. Space-separated list
  apiExcludes = 'types.raml' // Optional. Space-separated list
```

**Note:** This tool replaces the deprecated "generate-api-docs" (publishAPI) facility.
Do not use both.

Examples:

* [mod-courses](https://github.com/folio-org/mod-courses/blob/master/Jenkinsfile)
  -- RAML
  * Its [uprade PR](https://github.com/folio-org/mod-courses/pull/122). See each commit which explained each step.

#### Jenkinsfile for OAS

```
buildMvn {
...
  doApiDoc = true
  doApiLint = true
  apiTypes = 'OAS' // Required. Space-separated list: RAML OAS
  apiDirectories = 'src/main/resources/openapi' // Required. Space-separated list
  apiExcludes = 'headers' // Optional. Space-separated list
```

Examples:

* [mod-eusage-reports](https://github.com/folio-org/mod-eusage-reports/blob/master/Jenkinsfile)
  -- OAS
* [mod-search](https://github.com/folio-org/mod-search/blob/master/Jenkinsfile)
  -- OAS

