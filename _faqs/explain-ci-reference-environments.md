---
layout: page
title: Explain continuous integration for folio-snapshot-stable system
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: testing
faqOrder: 2
---

The software build procedure is [explained](/guides/automation/#software-build-pipeline) providing a diagram showing each stage, with explanation about how it is achieved, what time of day, and links to the resultant servers.

Various systems are regularly built. After `folio-snapshot` is built, if the suite of integration and regression tests pass, then the `folio-snapshot-stable` system is updated to match that.

