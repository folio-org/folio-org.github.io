---
layout: guidelines
title: Releasing
heading: Releasing
permalink: /guidelines/releasing/
---

The exact procedure for making a release is not yet specified. It is likely to
be something like we are doing for other software:

- Freeze the master for a short while
- Make a release branch
- Make changes specific for this release in the branch
- Tag a version
- Package and release it

Refer to the specific [Release procedures](/devguides/release-procedures).

Later, if there are bugs in the released version, work can continue on the
version branch, and we can release a new minor version from the branch. Some
changes may be cherry-picked from the master, or from the version branch to the
master, as need be.

