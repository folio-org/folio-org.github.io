---
layout: guidelines
title: Implementation Versions
heading: Implementation Versions
permalink: /guidelines/implementversions/
---

We follow the rules commonly known as [_semantic versioning_](http://semver.org/)
to version both FOLIO
_modules_ (aka _apps_) and any other FOLIO software components (e.g. utility libraries of frameworks),
so-called _non-modules_.

The implementation versions are three-part part numbers: _major.minor.bugfix_, such as `2.7.18`.

FOLIO _modules_ may implement more than one interface so they are versioned independently from any
particular interface, they need to however follow the same rules:

- For _modules_, the major part should be incremented if you implemented a backwards incompatible
  change to the API(s), (this will be indicated by the major number change in the particular API).
  For non-modules this may also mean any major changes with respect to functionality or implementation that don't
  necessarily result in interface changes, e.g. migration to a new DB backend.

- For _modules_ the middle part should be incremented if you implemented an addition to the API(s),
  (the minor version of the particular API has been changed).
  For non-modules it may also mean any additional functionality. For both, the change must be backwards compatible with
  respect to any client code or agents.

- For _modules_ the bugfix part should be incremented if you haven't changed anything in
  the API or added any new functionality but only fixed implementation bugs, etc. The same applies for _non-modules_.

