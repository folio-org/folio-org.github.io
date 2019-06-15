---
layout: page
title: Regular FOLIO releases
permalink: /guides/regular-releases/
menuInclude: no
menuTopTitle: Guides
---

The main set of FOLIO modules are coordinated to form a regular release.
At this stage it happens on a quarterly basis.
The approximates dates and descriptive names (e.g. bellis, clover, daisy) for upcoming releases are listed at [FOLIO Development Timeline Dates](https://wiki.folio.org/display/RPT/FOLIO+Development+Timeline+Dates).

The preparation for each release has a dedicated Slack [channel](/guidelines/which-forum/#slack)
(`#releases`). There are various planning documents pinned there.

The cut-off dates for module releases that are to be included, are also listed in those spreadsheets.

A typical strategy for a module development is to keep doing the normal work in feature branches and merging to master until its final release and cut-off date.

Hold off feature branches that are not to be included in the release.

At the specified dates, the platforms (with the lists of versions of modules) are tagged and branched to form the quarterly release.
The platform-core and platform-complete are branched, and declare the specific versions of each module.

For a module that is released to be part of a quarterly release, use a longer-term [branch](/guidelines/release-procedures/#bug-fix-releases) to track the bug fixes.
So this is an anticipated bug free and "stable" branch.
Any necessary bug-fix releases can be made from there.

Normal development can now continue, with feature branches merged to master.

