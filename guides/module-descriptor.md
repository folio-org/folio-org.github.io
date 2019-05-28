---
layout: page
title: ModuleDescriptor
permalink: /guides/module-descriptor/
menuInclude: no
menuTopTitle: Guides
---

This guide provides an overview of the ModuleDescriptor.

The ModuleDescriptor is introduced in the Okapi Guide
(e.g. [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#what-are-modules)
and [here](https://github.com/folio-org/okapi/blob/master/doc/guide.md#example-4-complete-moduledescriptor)).

The MD adheres to the [ModuleDescriptor.json](https://github.com/folio-org/okapi/blob/master/okapi-core/src/main/raml/ModuleDescriptor.json) schema.
Follow "mod-notes" as an example.

```
TODO: Provide brief explanations of each main section.
```

The "metadata" section provides some additional items.
Currently only two items, which are used to assist the generation of a documentation snippet for Hocker Hub:

* `containerMemory` -- A hint about the minimum amount of memory required to run this module.
The values correlate with that used by [folio-ansible](https://github.com/folio-org/folio-ansible/tree/master/group_vars) for the [reference environments](/guides/automation/#reference-environments).
Note that these installations have a small amount of data and low activity load.

* `databaseConnection` -- Whether this module utilises a database.

