---
layout: page
title: Increase visibility of module documentation
permalink: /guides/visibility-module-docs/
menuInclude: no
menuTopTitle: Guides
---

## Introduction

There are many individual modules hosted at FOLIO GitHub.
The [Source-code map](/source/map/) lists every module, and links to its relevant related documentation.

This enables all developers to easily discover the information that they need, to be able to work with each module.

As explained in the FAQ [Where is developer documentation located](/faqs/where-is-developer-documentation-located/), one of the principles of FOLIO module development is that module documentation is managed along with its source code.

The following sections provide some tips for module developers to improve the discoverability of their module documentation.

## Assemble source-code map

Note: This section is intended for FOLIO DevOps people.

Explanation about how the [Source-code map](/source/map/) index is assembled and maintained:

Details of each repository that is hosted at FOLIO GitHub are gathered automatically
(including information such as type of repository; does it have a "docs" directory; if backend, then does it have a "ramls" directory).
This collection is done occasionally as a FOLIO DevOps infrastructure
[job](https://github.com/folio-org-priv/folio-infrastructure/tree/master/verify-repo-config).
It is not yet automated, but is initiated manually.
The resulting JSON file is committed as the
[\_data/repos.json](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos.json) data file.

The data file
[\_data/repos-metadata.yml](https://github.com/folio-org/folio-org.github.io/tree/master/_data/repos-metadata.yml)
contains additional metadata about some specific repositories.
This information includes extra documentation links, beyond that gathered in the above-mentioned repos.json file (note that such links are intended as starting points, not to list every piece of documentation here).
Please send pull-requests to add documentation links for your repository.
The YAML structure is explained in the head of that file.
The tool "[yq](https://github.com/kislyuk/yq)" is useful for verifying YAML files (e.g. do `yq '.' repos-metadata.yml`).

Behind the scenes of the page
[source-code/map.md](https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/source-code/map.md)
the Jekyll Liquid program assembles and presents this page.

