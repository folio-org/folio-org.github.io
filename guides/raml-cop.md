---
layout: page
title: Use raml-cop to assess RAML, schema, and examples
permalink: /guides/raml-cop/
menuInclude: no
menuTopTitle: Documentation
---

For RAML-using server-side projects, use [raml-cop](https://github.com/thebinarypenguin/raml-cop) to assess the RAML and schema and examples.

## Installation

Install it globally to enable use on any project.

```shell
npm install -g raml-cop
```

Do that again occasionally to keep it up-to-date. Its package.json is well-configured so that it regularly updates its dependencies, especially raml-1-parser etc.

## Usage

Run it on any RAML file (e.g. `raml-cop ramls/loan-storage.raml`) or on multiple files with `raml-cop ramls/*.raml`

There is a shell script to facilitate raml-cop for any repository.
Copy [mod-notes/lint-raml-cop.sh](https://github.com/folio-org/mod-notes/blob/master/lint-raml-cop.sh)

That can also be run via a git pre-commit hook.

```shell
if git diff --cached --name-only | grep --quiet "/ramls/"
then
  exit 0
else
  ${GIT_DIR}/../lint-raml-cop.sh
fi
```

## Messages

The warning and error messages can sometimes be obscure.
See some examples below.

Heed the warning messages. They can often be more than that label implies. Some issues can mask others, so it is wise to fix them all.

### General interpretation notes

The line-numbers are zero-based, so the actual line-number is one more than reported.

### Example has additional properties

```shell
$ raml-cop ramls/configuration/config.raml
[ramls/raml-util/rtypes/collection.raml:19:29] WARNING Content is not valid according to schema: Additional properties not allowed: updatedDate,updatedBy
```

That line 20 is:

```
                example: <<exampleCollection>>
```

So in the config.raml file, investigate each "exampleCollection", and compare its example with its schema.

### Fix pathname to resultInfo.schema

```shell
$ raml-cop ramls/codex/codex.raml
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

Note: Do not use references with two sets of dot-dots.

