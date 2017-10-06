---
layout: guidelines
title: Coding Style
heading: Coding Style
permalink: /guidelines/codingstyle/
---

Follow the coding style that is being used by each repository for each
file type. Some projects do provide a `.editorconfig` file.

For Java code, we basically try to adhere to Sun Java coding
[conventions](http://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
(that document is old and unmaintained, but seems to be good enough as it is).

There are a few exceptions:

- We indent with two spaces only, because vert.x uses deeply nested callbacks.
- We _don't_ use tab characters for indents, only spaces.

For XML and JSON and RAML files, the same: two-space indent and no tabs.

Remember to set your IDE and editors to remove trailing spaces on saving files,
since those produce unnecessary diffs in Git.
Refer to coding style [configuration](/source/setup#coding-style) assistance.

For JSON key names we use camelCase.

For JavaScript code we are implementing an automated lint facility.
