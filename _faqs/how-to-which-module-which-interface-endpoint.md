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

## Registry of ModuleDescriptors

Use the FOLIO Registry to search for modules that provide or require certain interfaces.

This is particularly useful for developers who are about to make breaking changes, to determine which modules they are going to affect.

The API documentation for Okapi [explains](https://s3.amazonaws.com/foliodocs/api/okapi/p/okapi.html#proxy_modules_get) the query parameters.

Registry queries such as the following will assist investigation ...

### Interfaces provided by module

Confirm that a certain [back-end module](/source-code/map/#backend-mod) implements a certain interface which handles a set of endpoints.
Obtain its ModuleDescriptor from the registry and extract the "provides" section.
For example:

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-inventory-storage&latest=1&full=true' \
  | jq '.[].provides'
```

### Requires an old interface

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&require=instance-bulk%3D0.1'
```

### Provides a newer interface

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&provide=inventory-record-bulk'
```

## UI Developer Settings

The best facility at this stage of the project is provided by the [ui-developer](/source-code/map/#ui-developer) module.

Do login to the relevant running FOLIO system, and visit the "Settings : Developer : Okapi paths" page.
This will list the "resource path to interface mapper" for all of the modules configured for that FOLIO instance.<br/>
For example: [https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths](https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths)

Also the "resource path to permission-set mapper" shows which permissions are needed in order to access a certain endpoint:<br/>
[https://folio-snapshot.dev.folio.org/settings/developer/can-i-use](https://folio-snapshot.dev.folio.org/settings/developer/can-i-use)

Developers will also find other gems at the Developer Settings area.

