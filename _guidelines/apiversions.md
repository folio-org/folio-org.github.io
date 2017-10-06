---
layout: guidelines
title: API/Interface Versions
heading: API/Interface Versions
permalink: /guidelines/apiversions/
---

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
