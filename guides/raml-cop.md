---
layout: page
title: Use raml-cop to assess RAML, schema, and examples
permalink: /guides/raml-cop/
menuInclude: no
menuTopTitle: Guides
---

For RAML-using server-side projects, use [raml-cop](https://github.com/thebinarypenguin/raml-cop) to assess the RAML and schema and examples.

The [Primer for RAML and JSON Schema](/start/primer-raml/) provides some general guidance.

## Installation

Clone the "folio-tools" repository, and use its "lint-raml" scripts (see below).

Or install raml-cop globally to enable basic use on any project.

```shell
npm install -g raml-cop
```

Do that again occasionally to keep it up-to-date. Its package.json is well-configured so that it regularly updates its dependencies, especially raml-1-parser etc.

Integrate raml-cop with editors such as "Sublime Text".

## Usage

For basic use, run it on any RAML file (e.g. `raml-cop ramls/loan-storage.raml`) or on multiple files with `raml-cop ramls/*.raml`

There are also processing tools to assist RAML and schema maintenance for any FOLIO repository.
See the [folio-tools/lint-raml](https://github.com/folio-org/folio-tools/tree/master/lint-raml) directory.
The scripts utilise raml-cop and some also conduct other tests.
Use the Python script in preference -- that is the one used during continuous-integration (CI) via the `runLintRamlCop` [Jenkinsfile](/guides/jenkinsfile) parameter.

The CI job detects some issues before running 'raml-cop'. This helps to explain subsequent messages.

It also does some assessment of JSON Schema files, e.g. to encourage
[Describe schema and properties](/guides/describe-schema/).

## Messages

The warning and error messages from its raml-1-parser can sometimes be obscure.
See some examples below.

Heed the warning messages. They can often be more than that label implies. Some issues can mask others, so it is wise to fix them all.

### General interpretation notes

The line-numbers are zero-based, so the actual line-number is one more than reported.

### Example has additional properties

```shell
raml-cop ramls/configuration/config.raml
[ramls/raml-util/rtypes/collection.raml:19:29] WARNING Content is not valid according to schema: Additional properties not allowed: updatedDate,updatedBy
```

That line 20 is:

```
                example: <<exampleCollection>>
```

So in the config.raml file, investigate each "exampleCollection", and compare its example with its schema.

### Example has missing required properties

```shell
raml-cop ramls/calendar.raml
[ramls/raml-util/rtypes/collection.raml:17:25] WARNING Content is not valid according to schema: Missing required property: openings
```

That line 18 is:

```
                example: <<exampleCollection>>
```

So in the RAML file, investigate each "exampleCollection", and compare its example with its schema.

In this case the schema had the incorrect name for the required property.

### Fix pathname to resultInfo.schema

```shell
raml-cop ramls/codex/codex.raml
[ramls/codex/codex.raml:11:4] WARNING Can not parse JSON example: Unexpected end of JSON input
[ramls/codex/codex.raml:11:4] WARNING Can not parse JSON example: Unexpected end of JSON input
[rtypes/collection-get.raml:17:16] WARNING Can not parse JSON example: Unexpected end of JSON input
```

That line 18 in `collection-get.raml` is:

```
                example: <<exampleCollection>>
```

That line 11 in `codex.raml` declares the `instanceCollection` schema.
Its include path name is okay. So investigate the `$ref` inside it.

Need to use the actual pathname to the schema file located one directory above.

```
<       "$ref": "resultInfo.schema"
---
>       "$ref": "../resultInfo.schema"
```

Note: For pre-RMBv20 do not use references with two sets of dot-dots.

### No empty optional required section

If a JSON Schema does not have any properties that are required, then do not use an empty "required" array. Instead simply remove that optional "required" element.
Otherwise the raml-1-parser will try to be helpful with a message such as this:

```
[ramls/note.json:0:0] WARNING Invalid JSON schema: Remote reference didn't compile successfully: https://__/APPENDED_PROTOCOL/__/.../ramls/userDisplayInfo.json#
```

