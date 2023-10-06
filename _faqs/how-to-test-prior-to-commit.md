---
layout: page
title: How to run tests prior to commit
titleLeader: "FAQ |"
menuTopTitle: FAQs
categories: testing
faqOrder: 1
---

Developers are encouraged to run local tests before committing and pushing a branch.

Each front-end module has various tests (e.g. `yarn test` and `yarn lint`).

Each back-end module has unit tests (e.g. `mvn clean test`).

Some modules have additional local tests -- see their README document.

The Wiki page [ERM Unit Testing in RTL/Jest](https://wiki.folio.org/pages/viewpage.action?pageId=54887207) is a guide for writing unit tests for the UI modules within ERM, using RTL (React testing library) and the Jest test runner.
The notes there will also be useful for other modules.

See [Code analysis and linting facilities](/guides/code-analysis/).

The integration tests and regression tests for FOLIO UI are explained at 
[platform-complete](https://github.com/folio-org/platform-complete)
and
[stripes-testing](https://github.com/folio-org/stripes-testing)
along with the ability to run specific tests.

(The deprecated repository ui-testing [Regression tests for FOLIO UI](https://github.com/folio-org/ui-testing) might still be useful while tests and documentation are moved to those places.)

When running local tests, ensure a well-configured Stripes (see [Creating a new development setup for Stripes](https://github.com/folio-org/stripes/blob/master/doc/new-development-setup.md)). Ensure an up-to-date [Pre-built Vagrant box](https://github.com/folio-org/folio-ansible/blob/master/doc/index.md).
