---
layout: page
title: How to determine which module handles which interface and endpoint
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 8
---

This is not a easy topic in the new FOLIO multi-module system.
Techniques for gathering and navigating the relevant information are under development.

Jump to the current best facility, the [UI Developer Settings](#ui-developer-settings).

## API documentation

There is the set of [API documentation](/reference/api/) which is automatically generated from each separate back-end module's RAML files and JSON Schemas.
Developers could wade through that, making an educated guess.
(There are tickets in the Issue tracker to improve that aspect of the API documentation, but not happening yet.)

## ModuleDescriptors

Or developers could confirm that a certain [back-end module](/source-code/map/#backend-mod) provides a certain interface which handles a set of endpoints. Again an educated guess.
Obtain its ModuleDescriptor from the registry and extract the "provides" section.
For example:

```
curl -s -S -w'\n' \
  'http://folio-registry.aws.indexdata.com/_/proxy/modules?filter=mod-notes&latest=1&full=true' \
  | jq '.[].provides'
```

## UI Developer Settings

The best facility at this stage of the project is provided by the [ui-developer](/source-code/map/#ui-developer) module.

Do login to the relevant running FOLIO system, and visit the "Settings : Developer : Okapi paths" page.
This will list the "resource path to interface mapper" for all of the modules configured for that FOLIO instance.

For example:

[https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths](https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths)

Developers will also find other gems at the Developer Settings area.

