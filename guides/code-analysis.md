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

### Local use

The [SonarLint](http://www.sonarlint.org) extension for IDEs will detect quality issues at an early stage.

Use "Connected mode" to hook directly into our project rules.

### Rule customization

See an [example](https://github.com/folio-org/okapi/pull/367/commits/1710e99d574152cc67990d83d400951e8f11e309)
of using SuppressWarnings.

Regarding "Quality Profile" see issue [FOLIO-864](https://issues.folio.org/browse/FOLIO-864)

## ESLint for client-side projects

The [Code quality](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md#code-quality)
section of _The Stripes Module Developer's Guide_ explains ESLint usage, how to run it prior to commit, and how to disable some lines.

## RAML and Schema

For RAML-using server-side projects, [raml-cop](/guides/raml-cop/) assesses RAML and schema and examples.

## Other lint tools

These are not included in continuous integration, but are certainly useful as local tools.

For JSON files, [jq](https://github.com/stedolan/jq) is useful for validation, pretty-printing and linting, and for many JSON processing and viewing tasks.


