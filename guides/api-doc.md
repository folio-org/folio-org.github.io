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
Currently [RAML 1.0](/start/primer-raml/) and [OAS 3.0](/start/primer-oas/) are handled.

## Usage

For use during FOLIO CI builds, refer to the GitHub Workflows [configuration](#github-workflows) section below.
Note that the project should also use "[api-lint](/guides/api-lint/)" which utilises the same configuration for the [properties](#properties) apiTypes, apiDirectories, etc.)

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
* `-e,--excludes` -- List of additional sub-directories and/or files (just filenames, not paths) to be excluded (so that the tool will only discover top-level root API description files).
  Optional. Space-separated list.
  By default it excludes certain well-known directories (such as `raml-util examples headers parameters`).
  Use the option `--loglevel debug` to report what is being excluded.

Don't quote a space-separated list. Correct: `-e examples headers`. Wrong: `-e "examples headers"`. Wrong: `"-e examples headers"`.

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
  -e examples headers
```

Example for both RAML and OpenAPI (OAS), i.e. when preparing for transition:

```
cd $GH_FOLIO/mod-foo
python3 ../folio-tools/api-doc/api_doc.py \
  -t RAML OAS \
  -d ramls src/main/resources/oas
```

### GitHub Workflows

All relevant back-end repositories are now configured to use GitHub Workflows for the API-related tasks.
See the `.github/workflows` directory and the "Actions" UI tab.

The configuration [properties](#properties) are further described as comments in each workflow file.

Note the workflows only operate when there is a file change commit in their API descriptions directory.
Be sure to add to the "on: paths" sections of the workflow file.

NOTE: For back-end modules, also add the path to ModuleDescriptor, because the [api-doc](https://github.com/folio-org/folio-tools/tree/master/api-doc) facility interprets the MD to match the [endpoints to interfaces](/reference/api/endpoints/#interfaces).
Therefore the Workflow run will be triggered when the MD is modified.
(The edge-modules do not provide interfaces in their MD, so no need.)

NOTE: When preparing the pull-request, make a follow-up commit to one of the API description files. This is because the Actions runs are only triggered when those files are changed.

For a [new](/guidelines/create-new-repo/) project repository, follow the implementations for a similar repository.
(All were done via [FOLIO-3678](https://issues.folio.org/browse/FOLIO-3678)).
Some example PRs (but if copied, then do ensure that Workflow actions are updated - see note below):

* [mod-courses](https://github.com/folio-org/mod-courses/pull/157)
  -- RAML.
* [mod-settings](https://github.com/folio-org/mod-settings/pull/30)
  -- OAS.
* [mod-notes](https://github.com/folio-org/mod-notes/pull/240)
  -- OAS.
* [mod-calendar](https://github.com/folio-org/mod-calendar/pull/164)
  -- OAS. This one also needs to "exclude" some sub-directories.

Occasionally verify that your workflow files are up-to-date (e.g. for the versions of dependent "actions").
Compare with the default files at [folio-org/.github/workflow-templates](https://github.com/folio-org/.github/tree/master/workflow-templates).

### Jenkinsfile

<div class="attention">
NOTE: Using api-doc via Jenkins is <a href="https://issues.folio.org/browse/FOLIO-3678">deprecated</a>.
All relevant back-end repositories are now using GitHub Workflows for API-related operations.
</div>

<div class="folio-spacer-content"></div>

