---
layout: page
title: How to run tests prior to commit
titleLeader: "FAQ |"
menuTopTitle: Documentation
categories: testing
faqOrder: 1
---

Developers are encouraged to run local tests before committing and pushing a branch.

Each front-end module has various tests (e.g. `yarn test` and `yarn lint`).

Each back-end module has unit tests (e.g. `mvn clean test`).

Some modules have additional local tests -- see their README document.

See [Code analysis and linting facilities](/doc/code-analysis/).

The [Regression tests for FOLIO UI](https://github.com/folio-org/ui-testing) explains the overall testing framework. It also shows how tests can be run from each UI module. Ensure a well-configured Stripes (see [Creating a new development setup for Stripes](https://github.com/folio-org/stripes-core/blob/master/doc/new-development-setup.md)). Ensure an up-to-date [Pre-built Vagrant box](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md).
