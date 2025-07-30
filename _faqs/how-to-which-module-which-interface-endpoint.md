---
layout: page
title: How to determine which module handles which interface and endpoint
titleLeader: "FAQ |"
menuTopTitle: FAQs
categories: development-tips
faqOrder: 9
---

This is not a easy topic in the new FOLIO multi-module system.
Techniques for gathering and navigating the relevant information are under development.

## API documentation

There is the set of [API documentation](/reference/api/), and the associated list of [endpoints](/reference/api/endpoints/), which is automatically generated from each separate back-end module's API description files and JSON Schemas.

Also utilise the [Search API endpoints](/search-endpoints/) facility.

## API dependencies

[FOLIO API dependencies](https://dev.folio.org/folio-api-dependencies/). Tool for exploring module dependencies in FOLIO.

Tools and resources for managing and visualizing dependencies in the FOLIO API ecosystem. It includes a web-based interface for exploring module dependencies, API usage counts, and detailed API usage views.

See its [source-code](/source-code/map/#folio-api-dependencies).

## Registry of ModuleDescriptors

Use the FOLIO Registry to search for modules that provide or require certain interfaces.

This is particularly useful for developers who are about to make breaking changes, to determine which modules they are going to affect.

The API documentation for Okapi [explains](https://s3.amazonaws.com/foliodocs/api/okapi/p/okapi.html#proxy_modules_get) the query parameters.

Registry queries such as the following will assist investigation ...

### Interfaces provided by module

Confirm that a certain [back-end module](/source-code/map/#backend-mod) implements a certain interface which handles a set of [endpoints](/reference/api/endpoints/).
Obtain its ModuleDescriptor from the registry and extract the "provides" section.
For example:

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-inventory-storage&latest=1&full=true' \
  | jq -r '.[].provides'

curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?filter=mod-inventory-storage&latest=1&full=true' \
  | jq -r '.[].provides[] | [.id, .version] | @tsv'
```

### Requires an interface

Discover which modules are using a specific interface:

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&require=inventory-record-bulk' \
  | jq -r '.[].id'
```

### Requires an old interface

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&require=instance-bulk%3D0.1' \
  | jq -r '.[].id'
```

### Provides a newer interface

```
curl -s -S -w'\n' \
  'https://folio-registry.dev.folio.org/_/proxy/modules?latest=1&provide=inventory-record-bulk' \
  | jq -r '.[].id'
```

## UI Developer Settings

Some facilities are provided by the [ui-developer](/source-code/map/#ui-developer) module.

Do login to the relevant running FOLIO system, and visit the "Settings : Developer : Okapi paths" page.
This will list the "resource path to interface mapper" for all of the modules configured for that FOLIO instance.\
For example: [https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths](https://folio-snapshot.dev.folio.org/settings/developer/okapi-paths)

Also the "resource path to permission-set mapper" shows which permissions are needed in order to access a certain endpoint:\
[https://folio-snapshot.dev.folio.org/settings/developer/can-i-use](https://folio-snapshot.dev.folio.org/settings/developer/can-i-use)\
The paths which match the search will then link to the relevant module and to its section of the API documentation.

Developers will also find other gems at the Developer Settings area.

