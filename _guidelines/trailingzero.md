---
layout: guidelines
title: Trailing Zero
heading: Trailing Zero
permalink: /guidelines/trailingzero/
---

Changes to major and minor version follow from adding new features or larger
code refactoring, usually planned in advance. The bugfix version number is reserved for
tracking changes caused by malfunction that may be hard to predict.

As such, every new version for a particular major.minor series (e.g. `2.71`) start with bugfix
version set as 0, effectively `2.71.0`. This indicates that no bugs have been discovered (yet)
and no hotfix releases provided.

