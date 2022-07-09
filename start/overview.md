---
layout: page
title: Overview for a new developer
permalink: /start/overview/
menuInclude: yes
menuTopTitle: Start
menuSubTitle: New developer overview
menuSubIndex: 2
---

This is a high-level summary of "getting started" points for a new developer -- the on-boarding guide.

Note that each document has text that summarises, explains, and guides to other relevant documentation. So just following the links listed below is not sufficient. The order of the links is a loose sequence to becoming involved, setting up, and getting started (however note that many documents refer to each other and there is no strict sequence).

## Background orientation

[Getting started](/start/).
The main introduction and starting point.

[Guidelines overview : Background orientation](/guidelines/#background-orientation)
and
[Guides : Background orientation](/guides/#background-orientation)
and the other sections of those documents.

[Which forum to use for communication](/guidelines/which-forum/).
An overview of the [collaboration tools](/community/#collaboration-tools), how to register and participate.

[Search dev.folio.org and other searches](/search/).

[Frequently asked questions](/faqs/).

[Guidelines for Contributing Code](/guidelines/contributing/).

[Guidelines for FOLIO issue tracker](/guidelines/issue-tracker/).

[FOLIO Glossary](/reference/glossary/).

There are regular developer-related [news, events, and presentations](/community/events/).

The [FOLIO Forum: Fundamentals of the FOLIO Community](https://discuss.folio.org/t/folio-forum-fundamentals-of-the-folio-community/3102)
and other presentations in the [FOLIO Member Onboarding](https://www.youtube.com/hashtag/foliomemberonboarding) series.

Add yourself to the
[FOLIO Developer Directory](https://wiki.folio.org/display/COMMUNITY/FOLIO+Developer+Directory).
As requested in the [Slack forum guidelines](/guidelines/which-forum/#slack) please also improve your Slack identity information.

Become familiar with the general FOLIO web site.
Note that there is a common FOLIO-wide project navigation bar at the <a href="">top</a> of each of the various web sites.
Use its "Overview" menu to reach the "Community" section which provides other avenues to the starting points, and to subscribe to the monthly email newsletter for "Community updates".

For developers associated with the [OLE](/reference/glossary/#ole) partner institutions, become familiar with the [Open Library Environment](https://openlibraryenvironment.org/) web site, and follow some additional [OLE on-boarding](https://wiki.folio.org/display/COMMUNITY/Getting+Started+for+Developers) steps.

For developers associated with the [EPAM](https://wiki.folio.org/display/FOLIJET/Folio+Development+Teams+Home) teams, refer to various getting started and management documentation at that wiki area.

For groups of developers from other institutions, contact the [FOLIO Product Council](https://wiki.folio.org/display/PC/FOLIO+Product+Council).

The FOLIO Technical Council has a list of current [Technical Skills in Demand](https://wiki.folio.org/display/TC/Technical+Skills+in+Demand).

## Setup and configuration

[FOLIO uses any programming language](/guides/any-programming-language/).

[Guides : Setup and configuration](/guides/#setup-and-configuration).

[Guides : Setup development environment](/guides/developer-setup/).

[folio-ansible](https://github.com/folio-org/folio-ansible)
-- Development environment virtual machines.
And see more about that topic below.

[Source Code](/source-code/).
Overview descriptions and links to all repositories.
As explained there, each separate module also has a README with specific documentation.
Module documentation is kept with the relevant repository, while broad and project-wide documentation is here at the dev.folio.org site.

## Development documentation

[API documentation](/reference/api/).

[Fundamental documentation](/start/#fundamental-documentation).
This section links to some of the main other technical documentation starting points, which also link to related documentation.

[Primer documentation](/start/#primer-documentation).
These are concise documents to summarise and steer through getting started and lead to other getting started documentation.

[Okapi Guide and Reference](https://github.com/folio-org/okapi/blob/master/doc/guide.md).
The guide also has an accompanying shell script to run the examples to explain
and demonstrate a local Okapi instance.
The related [Securing Okapi](https://github.com/folio-org/okapi/blob/master/doc/guide.md#securing-okapi) explains and demonstrates the auth system.

[Folio-Sample-Modules](https://github.com/folio-org/folio-sample-modules)

[Tutorials : Using a FOLIO virtual machine](/tutorials/folio-vm/)
-- Explains how to utilise a FOLIO virtual machine (VM).

[RAML Module Builder (RMB) framework](https://github.com/folio-org/raml-module-builder).

[FOLIO Spring Base library](https://github.com/folio-org/folio-spring-base).

[mod-notes](https://github.com/folio-org/mod-notes) is
used in various documentation as a back-end exemplar.
Also its run.sh script to run a basic local system.

[Stripes](https://github.com/folio-org/stripes/blob/master/README.md).
It contains links to other related Stripes and UI development documentation.

[Stripes entities: packages, modules, apps and more](https://github.com/folio-org/stripes/blob/master/doc/modules-apps-etc.md).

[The Stripes Module Developer's Guide](https://github.com/folio-org/stripes/blob/master/doc/dev-guide.md).

[Stripes: quick start](https://github.com/folio-org/stripes/blob/master/doc/quick-start.md).

[Stripes CLI](https://github.com/folio-org/stripes-cli)
and its [Stripes CLI User Guide](https://github.com/folio-org/stripes-cli/blob/master/doc/user-guide.md).

[Commence a module - structure and configuration](/guides/commence-a-module/).
Explains a module directory layout and configuration, and links to relevant documentation.

Overview of the FOLIO [automation](/guides/automation/) and continuous integration (CI/CD).
The [software build pipeline](/guides/automation/#software-build-pipeline) with explanatory graphic and links to each of the continuously built FOLIO [reference environments](/guides/automation/#reference-environments) for demonstrations and further testing.
Overview of FOLIO [Jenkins](/guides/automation/#jenkins).

Developers will need some way to [run a local FOLIO instance](/guides/run-local-folio/) and to script test queries against it.

Become familiar with your team's Rancher "[developer scratch environment](/faqs/how-to-get-started-with-rancher/)".

[FAQ : How to run tests prior to commit](/faqs/how-to-test-prior-to-commit/).

## Getting help and helping

Having followed this guide to get started, you will now be familiar with some of the available resources and forums.
Being a self starter is surely admirable. Please do use the [search](/search/) facilities for this site and for GitHub, and for searching the [issue tracker](/guidelines/issue-tracker/#filters-and-search), and for [Slack](/guidelines/which-forum/#slack).

Spending some time listening to the Slack channels and visiting each user's profiles, you will begin to know who is who. Otherwise ask, and someone will direct you.

We are all your friends, and we were also getting started once. People are pleased to be able to assist.

Contacting developers directly via Slack is sometimes appropriate. Other times it will be better to raise your topic on the channels, where various people can help and others can listen and learn.

[Guides : Finding tasks to assist and contribute](/guides/find-tasks/).

As you followed the various documentation, there were probably some areas that were not quite clear. Please help to improve that.
We can make it more efficient for everybody.

So welcome on board FOLIO as a new developer.
Please help to guide us all.

