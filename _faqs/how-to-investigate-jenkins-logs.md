---
layout: page
title: How to investigate Jenkins build logs
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 12
---

When a Jenkins build job fails (for example when building the reference environments, or build-platform-complete-snapshot) then developers will need to investigate the Jenkins output logfile.

The following are some tips.

Visit Jenkins for the relevant job. For example, follow the "job" links for [reference environment](/guides/automation/#reference-environments) builds.

Select the relevant failed build from the left-hand panel "Build History" section (e.g. `#847-folio-snapshot`).

In its left-hand panel, select "View as plain text". Then save the page to local, e.g. `~/Downloads/consoleText`).

Now use 'grep' or some such to detect certain patterns:

```shell
cat ~/Downloads/consoleText | egrep "Connection refused:|Incompatible version|Missing dependency:|Invalid URL path requested|no such image:|Timed out after waiting" > tmp1
```

```shell
cat ~/Downloads/consoleText | egrep "failed:|fatal:" > tmp2
```

Now inspect those temporary files.
Report the problems to the relevant project issue tracker.

