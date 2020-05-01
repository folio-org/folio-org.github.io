---
layout: page
title: Regular FOLIO releases
permalink: /guides/regular-releases/
menuInclude: no
menuTopTitle: Guides
---

The main set of FOLIO modules are co-ordinated to form a regular release.
At this stage it happens on a quarterly basis.

Refer to the [Releases](https://wiki.folio.org/display/REL/) area of the Wiki for co-ordination of the next release.
The approximate dates and descriptive flower-based names (e.g. Edelweiss, Fameflower, Goldenrod) for upcoming releases are also listed there.

The preparation for each release has a dedicated Slack [channel](/guidelines/which-forum/#slack)
(`#releases`). There are various planning documents pinned there.

The cut-off dates for module releases that are to be included, are also listed in those spreadsheets.

Refer to the [community release notes](https://wiki.folio.org/display/COMMUNITY/Release+Notes)
for important upgrade considerations.
Follow the [process](https://wiki.folio.org/pages/viewpage.action?pageId=36572486) for maintenance of those documents.

A typical strategy for a module development is to keep doing the normal work in feature branches and merging to master until its final release and cut-off date.

Hold off feature branches that are not to be included in the release.

At the specified dates, the platforms (with the lists of the specific release versions of modules) are tagged and branched to form the quarterly release.
The FOLIO Release is built daily as part of the [reference environments](/guides/automation/#reference-environments).

For a module that is released to be part of a quarterly release, use a longer-term [branch](/guidelines/release-procedures/#bug-fix-releases) to track the bug fixes.
So this is an anticipated bug free and "stable" branch.
Any necessary bug-fix releases can be made from there.

Normal development can now continue, with feature branches merged to master.

