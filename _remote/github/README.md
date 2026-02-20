---
layout: null
---

# Shared GitHub Workflows for FOLIO

## Introduction

The directory [`.github/workflows`](.github/workflows) contains the centralized workflows.

The directory [`workflow-templates`](workflow-templates) contains templates for some general CI/CD workflows.

## Status

The front-end `ui-` and `stripes-` repositories are currently being migrated to the centralized "UI" workflows.

The back-end Maven-based repositories are currently being migrated to the centralized "Maven" workflows [FOLIO-4443](https://folio-org.atlassian.net/browse/FOLIO-4443).

Workflows for Go-based back-end repositories are implemented for mod-reporting.

Centralized workflows are still to be developed to replace the old API workflow templates.

## Documentation

Refer to the various types of centralized workflows, including their setup and configuration:

* [README-UI.md](README-UI.md) -- for the front-end repositories.
* [README-docker.md](README-docker.md) -- for repositories that only have a Dockerfile.
* [README-go.md](README-go.md) and [README-go-lint.md](README-go-lint.md) -- for Go-based back-end repositories.
* [README-maven.md](README-maven.md) -- for Maven-based back-end repositories.

## Development

### Use actionlint prior to commit

Install [actionlint](https://github.com/rhysd/actionlint#quick-start).

While developing Workflows run actionlint prior to each commit. It is very helpful for identifying syntax and mis-configuration problems, which are otherwise difficult to diagnose.

It includes "shellcheck". The following typical invocation skips some well-known shellcheck basic issues:

```
SHELLCHECK_OPTS='--exclude=SC2086,SC2046' actionlint *.yml
```

There is an automated workflow that will run `actionlint` on pull-requests.

## Further information

* [Release procedure](docs/release-procedure.md)

