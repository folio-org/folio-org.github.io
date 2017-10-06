---
layout: guidelines
title: Module Implements One Interface
heading: Module Implements One Interface
permalink: /guidelines/moduleoneinterface/
---

In the simplest case, a module implements just one interface, but since we want to be able to register any functional changes to the module by
increasing the module's minor version number, we will keep two independent versions for the API and implementation. For example, a module with version `2.71.0`
may implement the checkout API at `3.14`. When the checkout API changes to `3.15`, and the module implements the change,
the module version becomes `2.72.0`. In the case where only the implementation is corrected (bugfixes with no functionality changes)
and the module still implements the checkout API at `3.14`, then the module version gets bumped to `2.71.1`.

