---
layout: page
title: Increase visibility of module documentation
permalink: /guides/visibility-module-docs/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

There are many individual modules hosted at FOLIO GitHub.
The [Source-code map](/source-code/map/) lists every module, and links to its relevant related documentation.

This enables all developers to easily discover the information that they need, to be able to work with each module.

As explained in the FAQ [Where is developer documentation located](/faqs/where-is-developer-documentation-located/), one of the principles of FOLIO module development is that module documentation is managed along with its source code.

The following sections provide some tips for module developers to improve the discoverability and usability of their module documentation.

## Overview

The [Source-code map](/source-code/map/) is automatically generated.
Each week an infrastructure [job](#assemble-source-code-map) gathers essential metadata about each project repository that is hosted at [FOLIO GitHub](https://github.com/folio-org).
Additional metadata is appended, which includes links to Wiki "App tips" and "App settings".
(The future "User docs" project may also provide relevant links.)

Would module developers please use the hints in the sections below to assist the bot to provide a useful repository listing.

## Docs directory

A top-level directory named "docs" or "doc" will be detected.

See examples:
[ui-courses](/source-code/map/#ui-courses)
and [mod-circulation](/source-code/map/#mod-circulation)
and [stripes-core](/source-code/map/#stripes-core).

Add a "docs" front page by creating a file in that directory named README.md (or README.rst).
GitHub will automatically display the contents of that page (whereas it will not display a file named index.md).

Use this front page to provide an index to the module's local documentation.

## The "About" section

GitHub provides a repository Setting called "About" at the top-right of each repository's front page.
Use this for a concise note about the purpose.

See examples:
[raml-module-builder](/source-code/map/#raml-module-builder)
and [ui-search](/source-code/map/#ui-search).

## The README introduction

Provide an "Introduction" or "Overview" as the first sub-section of the repository's top-level README page.

Especially utilise the first couple of sentences to provide a concise explanation of the features of the repository.

The bot could (TODO: not yet happening) gather the first 200 characters.

Note that if a template was used to generate the initial project content (e.g. using stripes-cli) then the boilerplate content needs to be replace at various parts of the initial README.

## Additional metadata

The data file
"[`_data/repos-metadata.yml`](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos-metadata.yml)"
contains additional metadata about some specific repositories.

This information includes extra documentation links, beyond that automatically gathered in the above-mentioned repos.json file.

Note that such links are intended as starting points, not to list every piece of documentation here.

Please send pull-requests to add documentation links for your repository.

The YAML structure is explained in the head of that file.
The tool "[yq](https://github.com/kislyuk/yq)" is useful for verifying YAML files (e.g. do `yq '.' repos-metadata.yml`

```
# name: This is the name of the GitHub repository, e.g. ui-users
#   urlUserTips: URL of the most relevant FOLIOtips Wiki page.
#   urlAppSettings: URL of the most relevant FOLIOtips/Settings Wiki page.
#   furtherDescription: Additional text to supplement repo GitHub About.
#   urlsOther: Array of other doc URLs.
```

## Improvements needed

If the FOLIO Wiki "[FOLIOtips](https://wiki.folio.org/display/FOLIOtips)" and "[FOLIOtips/Settings](https://wiki.folio.org/display/FOLIOtips/Settings)" index pages reliably used the module name (e.g. Tags for ui-tags) then the bot could automatically link, and so those attributes could be removed from the "[Additional metadata](#additional-metadata)" file.

Eventually there might be "App store" categories that could be use to cross-link such information.

Gather the first 200 characters of the Introduction section of each repository README page.

## Assemble source-code map

Note: This section is intended for FOLIO DevOps people.

Explanation about how the [Source-code map](/source-code/map/) index is assembled and maintained:

Details of each repository that is hosted at FOLIO GitHub are gathered automatically
(including information such as type of repository; does it have a "docs" directory; if backend, then does it have a "ramls" directory).
This collection is done occasionally as a FOLIO DevOps infrastructure
[job](https://github.com/folio-org-priv/folio-infrastructure/tree/master/verify-repo-config).
It is not yet automated, but is initiated manually.
The resulting JSON file is committed as the
"[`_data/repos.json`](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos.json)" data file.

The data file
"[`_data/repos-metadata.yml`](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos-metadata.yml)"
contains additional metadata about some specific repositories.

Behind the scenes of the page
"[`source-code/map.md`](https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/source-code/map.md)"
the Jekyll Liquid program assembles and presents this page.

Use the [Link checker](https://github.com/folio-org/folio-org.github.io/#link-checker) to verify internal and external links.

