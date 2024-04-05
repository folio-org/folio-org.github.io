---
layout: page
title: Assess API descriptions, schema, and examples
permalink: /guides/api-lint/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

For server-side projects that utilise RAML or OpenAPI (OAS), use the tool `api-lint` to assess the API description files and schema and examples.

The tool is available for use during FOLIO Continuous Integration builds, and also for local use prior to commit.
Currently [RAML 1.0](/start/primer-raml/) and [OAS 3.0](/start/primer-oas/) are handled.

## Procedure

Each discovered API description file is provided to the nodejs script.

That utilises the AML Modeling Framework [AMF](https://github.com/aml-org/amf), specifically the `amf-client-js` library, to parse and validate the definition.

Note: Some modules might find new violations being reported.
Refer to [Interpretation of messages](#interpretation-of-messages) below.

## Usage

For use during FOLIO CI builds, refer to the GitHub Workflows [configuration](#github-workflows) section below.
Note that the project should also use "[api-doc](/guides/api-doc/)" which utilises the same configuration for the [properties](#properties) apiTypes, apiDirectories, etc.)

For local use, clone the "[folio-tools](https://github.com/folio-org/folio-tools)" repository parallel to clones of back-end project repositories, and use its [api-lint](https://github.com/folio-org/folio-tools/tree/master/api-lint) facilities.
Refer to that document for local installation instructions.

### Python

The Python script will search the configured directories to find relevant API description files, and will then call the node script to process each file.

<a id="properties"></a>Where the main options are:

* `-t,--types` -- The type of API description files to search for.
  Required. Space-separated list.
  One or more of: `RAML OAS`
* `-d,--directories` -- The list of directories to be searched.
  Required. Space-separated list.
* `-e,--excludes` -- List of additional sub-directories and/or files to be excluded (so that the tool will only discover top-level root API description files).
  Optional. Space-separated list.
  By default it excludes certain well-known directories (such as `raml-util schema schemas examples headers parameters`).
  Use the option `--loglevel debug` to report what is being excluded.
* `-w,--warnings` -- Cause "warnings" to fail the workflow, in the absence of "violations".
  Optional. By default, if there are no "violations", then the workflow is successful and so any "warnings" would not be displayed.

See help for the full list:

```
python3 ../folio-tools/api-lint/api_lint.py --help
```

Example for RAML:

```
cd $GH_FOLIO/mod-courses
python3 ../folio-tools/api-lint/api_lint.py \
  -t RAML \
  -d ramls
```

Example for OAS:

```
cd $GH_FOLIO/mod-eusage-reports
python3 ../folio-tools/api-lint/api_lint.py \
  -t OAS \
  -d src/main/resources/openapi \
  -e headers
```

Example for both RAML and OpenAPI (OAS), i.e. when preparing for transition:

```
cd $GH_FOLIO/mod-foo
python3 ../folio-tools/api-lint/api_lint.py \
  -t RAML OAS \
  -d ramls src/main/resources/oas
```

### Node

The node script can also be used stand-alone to process a single file.

See usage notes with: `node amf.js --help`

### GitHub Workflows

All relevant back-end repositories are now configured to use GitHub Workflows for the API-related tasks.
See the `.github/workflows` directory and the "Actions" UI tab.

The configuration [properties](#properties) are further described as comments in each workflow file.

Note the workflows only operate when there is a file change commit in their API descriptions directory.

For a [new](/guidelines/create-new-repo/) project repository, follow the implementations for a similar repository.
(All were done via [FOLIO-3678](https://issues.folio.org/browse/FOLIO-3678)).
Some example PRs:

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
NOTE: Using api-lint via Jenkins is <a href="https://issues.folio.org/browse/FOLIO-3678">deprecated</a>.
All relevant back-end repositories are now using GitHub Workflows for API-related operations.
</div>

## Reports

At GitHub, detected issues are listed at the "Actions" tab.
For any branch or pull-request build, follow the "details" link via the coloured checkmark (or orange dot while building).

## Ensure valid JSON Schema

While api-lint can detect many issues with broken JSON Schema, it is advisable to ensure that the schema are valid locally before pushing changes to CI.
Otherwise the messages from api-lint can be confusing.

There are many schema validation tools. One such is
[z-schema](https://github.com/zaggino/z-schema):

```
for f in schema/*.json; do z-schema --pedanticCheck $f; done
```

Of course it is also advisable to follow on to verify the API descriptions locally with api-lint before pushing to continuous integration.

## Interpretation of messages

When errors are encountered, then a summary of conformance "Violations" and "Warnings" is presented at the top, followed by detail about each.
The detail includes the location of the relevant file and the line number of the problem.

Note that if there are only warnings but no violations, then nothing is presented.
Use the `--warnings` option described above.

