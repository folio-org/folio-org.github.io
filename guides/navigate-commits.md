---
layout: page
title: Navigation of commits and CI via GitHub and Jenkins
permalink: /guides/navigate-commits/
menuInclude: no
menuTopTitle: Guides
---

These are some tips for following the continuous integration [process](/guides/automation/).
This is useful for a successful build to understand the full process. Of course it is especially important in the case of a failure with your changes.

This scenario shows a developer pushing to a branch. Other scenarios would be similar, and each project could be different, and have additional CI processes. These examples just follow the Jenkins part.

Each set of changes at GitHub will initiate the process (e.g. branch push, pull request). The action can be followed in two ways.

* Visit the Slack channel [#folio-ci](/guidelines/which-forum/#slack) where a Start notification will have been sent.
An end status notification will soon follow. Each has a link directly to its Jenkins output.

* Visit the project's GitHub page at its "commits" tab, and select the relevant branch.
There will be the orange dot symbol while the CI is operating, and green tick or red cross when finished. Follow its link to its Jenkins details output.

Jenkins might also have sent an email notification in the case of a serious or unexpected build failure.

At the project's Jenkins build output page, follow the links to each of its Pipeline steps to see the detail. There are two views: the Classic view, or the Open Blue Ocean view. There is also history of previous builds.

There are some additional facilities available after login to Jenkins.
Jenkins credentials utilize the Github authentication for FOLIO core developers, so ensure that you are logged in to GitHub to then enable login to Jenkins.

For the merge to master, an additional set of processes will operate, as specified in the project's top-level [Jenkinsfile](/guides/jenkinsfile/).

