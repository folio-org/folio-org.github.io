---
layout: guidelines
title: Version Numbers
heading: Version Numbers
permalink: /guidelines/versioning/
---

# Versioning

Since (almost) all components have hard separation between interface and implementation,
we need to keep two kinds of version numbers, one for the API, and one for the implementation code.
To make matters worse, any FOLIO module may implement several interfaces.

## API/Interface Versions

The API versions are two-part _major.minor_ numbers, such as `3.14`

The rules are simple:

- If you only add things to the interface -- e.g. a new resource or method on existing resources --
  then you increment the minor number, because the API is backwards compatible.
- If you remove or change anything, you must increment the major number,
  because now your API is no longer backwards compatible.

For example, you can add a new resource to `3.14`, and call it `3.15`.
Any module that requires `3.14` can also use `3.15`. But if you remove
anything from the API, or change the meaning of a parameter, you need to
bump the API version to `4.1`

## Implementation Versions

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

## Module for One Interface

In the simplest case, a module implements just one interface, but since we want to be able to register any functional changes to the module by
increasing the module's minor version number, we will keep two independent versions for the API and implementation. For example, a module with version `2.71.0`
may implement the checkout API at `3.14`. When the checkout API changes to `3.15`, and the module implements the change,
the module version becomes `2.72.0`. In the case where only the implementation is corrected (bugfixes with no functionality changes)
and the module still implements the checkout API at `3.14`, then the module version gets bumped to `2.71.1`.

## Module for Multiple Interfaces

A module can implement more than one interface, and more than one major version
of any of them. In that case the version numbering is necessarily more complex.
Again, there does not have to be any correlation between the module version and the
version of the interfaces it implements.

For example, if the circulation module version `2.71.0` can implement the
checkout API version `3.14` and the checkin API version `1.41` then the
rules are still the same:

- If the change doesn't follow any change to any API and is merely a bugfix, increment the last part to `2.71.1`
- If you add new features that e.g. follow the extended APIs, increment the middle part to `2.72.0`
- If you implement any backwards-incompatible change to _any_ API, or drop _any_
  API at all, increment the module version to `3.0.0`

The most common case is probably when we need to add a new, incompatible API
to a module, but want to keep the old one too. In such cases we only increment
the module version to `2.72.0` but mark that it provides the API versions
`3.14` and `1.41`

## Trailing Zero

Changes to major and minor version follow from adding new features or larger
code refactoring, usually planned in advance. The bugfix version number is reserved for
tracking changes caused by malfunction that may be hard to predict.

As such, every new version for a particular major.minor series (e.g. `2.71`) start with bugfix
version set as 0, effectively `2.71.0`. This indicates that no bugs have been discovered (yet)
and no hotfix releases provided.