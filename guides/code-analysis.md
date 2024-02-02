---
layout: page
title: Code analysis and linting facilities
permalink: /guides/code-analysis/
menuInclude: no
menuTopTitle: Guides
---

All code repositories have linter and code-style analysis facilities implemented as part of their continuous integration. The pull requests will run the relevant static code analysis tools.

This document explains those facilities and shows how to run tools locally before pushing changes.

The client-side projects use "ESLint".
The server-side projects use "SonarQube".
Actually, the SonarQube [analysis](https://sonarcloud.io/organizations/folio-org/projects)
reports are available for all projects, and provide additional useful analysis.

## Preparing pull requests

The pull request will show the analysis messages of any new issues that arise from these code changes.

At this stage the contraventions will not prevent the merge to master.

Developers can minimise these reports by running the tools locally,
and in some cases configuring the code lines to avoid certain tests.

## SonarQube

[sonarcloud.io/organizations/folio-org](https://sonarcloud.io/organizations/folio-org/projects)

See [FOLIO-858](https://issues.folio.org/browse/FOLIO-858) to encourage 'A' ratings.

See [FOLIO-1049](https://issues.folio.org/browse/FOLIO-1049) to encourage 'A' ratings,
80% test coverage, and less than 3% duplicated lines.

Refer to project [configuration](/faqs/how-to-integrate-coverage-reports/) information.

### Local use

The [SonarLint](https://www.sonarlint.org) extension for IDEs will detect quality issues at an early stage.

Use "Connected mode" to hook directly into our project rules.

### Rule customization

Sonar may report false positives.  These should be suppressed in the source code.
The code review should include whether the suppression is correct.

In Java code use `@SuppressWarnings` at the variable or method level.  Avoid it at the class level
because variables and methods might be added in future that should receive warnings.

[Variable level example](https://github.com/folio-org/raml-module-builder/blob/v35.0.0/domain-models-maven-plugin/src/main/java/org/folio/rest/tools/ClientGenerator.java#L59-L60):

```
  @SuppressWarnings("squid:S1075")  // suppress "URIs should not be hardcoded"
  public static final String  PATH_TO_GENERATE_TO    = "/target/generated-sources/raml-jaxrs/";
```

[Method level example](https://github.com/folio-org/raml-module-builder/blob/v35.0.0/cql2pgjson/src/main/java/org/folio/cql2pgjson/util/Cql2SqlUtil.java#L36-L37):

```
  @SuppressWarnings("squid:S3776")  // suppress "Cognitive Complexity of methods should not be too high"
  public static String cql2like(String s) {
```

[Multiple suppressions example](https://github.com/folio-org/raml-module-builder/blob/v35.0.0/cql2pgjson-cli/src/main/java/org/z3950/zing/cql/cql2pgjsoncli/CQL2PGCLIMain.java#L29-L33):

```
  @SuppressWarnings({
    "squid:S1148",  // suppress "Use a logger to log this exception." because it's a CLI
    "squid:S106",   // suppress "Replace this use of System.out or System.err by a logger." because it's a CLI
  })
  public static void main( String[] args ) {
```

When Sonar reports an issue click on the rule to show the rule ID like squid:S1075.

Always add:

1. A comment with the human readable rule description as the rule ID is not self-explanatory.

1. A justification for the suppression.

Don't use `// NOSONAR` and don't use `@SuppressWarnings("all")`, they suppress all current and future rules.
Sonar continuously adds new rules, including security rules, that should trigger warnings.

Regarding "Quality Profile" see issue [FOLIO-864](https://issues.folio.org/browse/FOLIO-864)

## ESLint for client-side projects

The [Code quality](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md#code-quality)
section of _The Stripes Module Developer's Guide_ explains ESLint usage, how to run it prior to commit, and how to disable some lines.

## RAML and Schema

For RAML-using server-side projects, [api-lint](/guides/api-lint/) assesses RAML API descriptions and schema and examples.

The tools can be used in FOLIO CI, and locally prior to commit.

## OpenAPI and Schema

For OpenAPI-using server-side projects, [api-lint](/guides/api-lint/) assesses OAS API descriptions and schema and examples.

The tools can be used in FOLIO CI, and locally prior to commit.

## Other lint tools

These tools are not directly included in continuous integration, but are certainly also useful as local tools.

For JSON files, [jq](https://github.com/stedolan/jq) is useful for general validation, pretty-printing and linting, and for many JSON processing and viewing tasks.

JSON Schema validator such as [z-schema](https://github.com/zaggino/z-schema).
See example use for local maintenance of [ModuleDescriptors](/guides/module-descriptor).


