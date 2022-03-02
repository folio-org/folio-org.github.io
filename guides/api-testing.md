---
layout: page
title: Conduct API testing
permalink: /guides/api-testing/
menuInclude: no
menuTopTitle: Guides
---

The [folio-api-tests](https://github.com/folio-org/folio-api-tests) repository provides Postman collections for backend modules.

Developers should establish a baseline set for their module at [folio-api-tests](https://github.com/folio-org/folio-api-tests)
and thereafter keep it up-to-date when adding or updating interfaces and endpoints.

These sets of command-line tests can be run locally using [Newman](https://github.com/postmanlabs/newman)
against one of the pre-built Vagrant boxes VMs (e.g. [folio/snapshot](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md#prebuilt-vagrant-boxes)
and the upcoming [lighter-weight core VM](https://issues.folio.org/browse/FOLIO-1632)).

Such API tests are an important way to test because they interact directly with the running module and so circumvent the additional layers of user-interface type of tests.

The [api-lint](/guides/api-lint/) tool is useful to statically verify API description files and schemas and a small set of samples. These API tests operate as real-life testing.

