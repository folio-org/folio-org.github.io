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

For [RAML-using](/start/primer-raml/) projects, this new "api-lint" tool is preferred. The previous tool "[lint-raml](/guides/raml-cop/)" is still available. However its behind-the-scenes technology is outdated.

## Procedure

Each discovered API description file is provided to the nodejs script.

That utilises the AML Modeling Framework [AMF](https://github.com/aml-org/amf), specifically the `amf-client-js` library, to parse and validate the definition.

Note: Some modules might find new violations being reported.
Refer to [Interpretation of messages](#interpretation-of-messages) below.

## Usage

For use during FOLIO CI builds, refer to the Jenkinsfile [configuration](#jenkinsfile) below.

For local use, clone the "[folio-tools](https://github.com/folio-org/folio-tools)" repository parallel to clones of back-end project repositories, and use its [api-lint](https://github.com/folio-org/folio-tools/tree/master/api-lint) facilities.
Refer to that document for local installation instructions.

### Python

The Python script will search the configured directories to find relevant API description files, and will then call the node script to process each file.

Where the main options are:

* `-t,--types` -- The type of API description files to search for.
  Required. Space-separated list.
  One or more of: `RAML OAS`
* `-d,--directories` -- The list of directories to be searched.
  Required. Space-separated list.
* `-e,--excludes` -- List of additional sub-directories and files to be excluded.
  Optional. Space-separated list.
  By default it excludes certain well-known directories (such as `raml-util`).
  Use the option `--loglevel debug` to report what is being excluded.

See help for the full list:

```
python3 ../folio-tools/api-lint/api_lint.py --help
```

Example for RAML:

```
cd $GH_FOLIO/mod-notes
python3 ../folio-tools/api-lint/api_lint.py \
  -t RAML \
  -d ramls
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

### Jenkinsfile

To use "api-lint" with FOLIO Continuous Integration, add this configuration to the project's [Jenkinsfile](/guides/jenkinsfile/):

```
buildMvn {
...
  doApiLint = true
  apiTypes = 'RAML' // Required. Space-separated list: RAML OAS
  apiDirectories = 'ramls' // Required. Space-separated list
  apiExcludes = 'types.raml' // Optional. Space-separated list
```

**Note:** This tool replaces the deprecated "lint-raml" (runLintRamlCop) facility.
Do not use both.

Examples:

* [mod-tags](https://github.com/folio-org/mod-tags/blob/master/Jenkinsfile)
  -- RAML
* [mod-search](https://github.com/folio-org/mod-search/blob/master/Jenkinsfile)
  -- OAS
* [mod-quick-marc](https://github.com/folio-org/mod-quick-marc/blob/master/Jenkinsfile)
  -- both RAML and OAS

## Reports

At GitHub, detected issues are listed on the front page of each pull-request.
For any branch or pull-request build, follow the "details" link via the coloured checkmark (or orange dot while building) through to Jenkins.
Then see "Artifacts" at the top-right for the processing report.
Or follow across to Jenkins "classic" view, and find the report in the left-hand panel.

## Interpretation of messages

When errors are encountered, then a summary of conformance "Violations" and "Warnings" is presented at the top, followed by detail about each.
The detail includes the location of the relevant file and the line number of the problem.

Note that if there are only warnings but no violations, then nothing is presented.

Note that this `api-lint` tool is more thorough than our previous CI tool (based on raml-cop and its underlying raml-1-parser).
So projects might find new violations being reported.
(See some migration issues at [FOLIO-3017](https://issues.folio.org/browse/FOLIO-3017).)

