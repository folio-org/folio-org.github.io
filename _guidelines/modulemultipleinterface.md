---
layout: guidelines
title: Module Implements Multiple Interfaces
heading: Module Implements Multiple Interfaces
permalink: /guidelines/modulemultipleinterface/
---

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

