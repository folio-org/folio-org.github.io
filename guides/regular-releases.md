---
layout: page
title: Regular FOLIO releases
permalink: /guides/regular-releases/
menuInclude: no
menuTopTitle: Guides
---

The main set of FOLIO modules are co-ordinated to form a regular release.
At this stage it happens on an approximate quarterly basis.
(The normal [release procedure guidelines](/guidelines/release-procedures) still apply for individual module releases.)

Refer to the [Releases](https://wiki.folio.org/display/REL/) area of the Wiki for co-ordination of the next regular release, and for followup bugfix and hotfix release processes.
The approximate dates and names for upcoming releases are also listed there, along with calendars and milestone deadlines to assist planning.
Refer to the list of descriptive [flower-inspired names](https://wiki.folio.org/display/REL/Flower+Release+Names) (e.g. quesnelia, ramsons, sunflower, trillium).

The wiki page [Release process in Jira](https://wiki.folio.org/display/REL/Release+process+in+Jira) explains the use of the special issue tracker process to manage release related activities, and to track interface versions and RMB versions.
There is also a "Release board" to assess the current state.

The preparation for each release has a dedicated [Slack channel](/guidelines/which-forum/#slack)
(`#folio-releases`). There are various planning documents and spreadsheets pinned there.
Notification of each individual module release is sent to this channel, as well as other important announcements and co-ordination.

The cut-off dates for module releases that are to be included, are also listed in those spreadsheets.

Refer to the [Cross Release Statistics](https://wiki.folio.org/display/REL/Cross+Release+Statistics)
for important upgrade considerations.
Follow the [process](https://wiki.folio.org/pages/viewpage.action?pageId=36572486) for maintenance of those documents.

The quality assurance state of each module is listed at the
[FOLIO Quality Dashboard](https://wiki.folio.org/display/DQA/FOLIO+Quality+Dashboard).

A typical strategy for a module development is to keep doing the normal work in feature branches and merging to master until its final release and cut-off date.

Hold off feature branches that are not to be included in the release.

At the specified dates, the platforms (with the lists of the specific release versions of modules) are tagged and branched to form the quarterly release.
The FOLIO Release is built daily as part of the [reference environments](/guides/automation/#reference-environments).

For a module that is released to be part of a quarterly release, use a longer-term [branch](/guidelines/release-procedures/#bug-fix-releases) to track the bug fixes.
So this is an anticipated bug free and "stable" branch.
Any necessary bug-fix releases can be made from there.

Normal development can now continue, with feature branches merged to master.

