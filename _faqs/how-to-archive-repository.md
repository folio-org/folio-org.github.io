---
layout: page
title: How to archive a GitHub repository
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: management
faqOrder: 4
---

## Introduction

If a repository is no longer maintained, and a decision has been made to archive the repository, then follow this procedure.

(**Note**: If the repository is to be **renamed** rather than archived, then there are various ramifications.
Tread very carefully and follow the guide [Rename a module](/guides/rename-module/) instead.)

## Raise a Jira ticket

Create a Jira ticket so that people are aware of what happened to the repository.

Certain operations will require Admin access to the repository.
Ask at Slack #devops channel.

Alternatively, set the "Development team" for the Jira ticket to be "FOLIO DevOps", and then that team will handle it.
Explain in the ticket what needs to happen, e.g. provide text for the README notice.

## Ensure not in a Platform

Ensure that this module is not in a Stripes Platform,
i.e. search in the [platform-complete install.json](https://github.com/folio-org/platform-complete/blob/snapshot/install.json) generated file.

Its functionality should have already moved to other modules.
If still present, then verify that no other module depends upon it
(e.g. search the [Registry of ModuleDescriptors](/faqs/how-to-which-module-which-interface-endpoint/#registry-of-moduledescriptors)).

If needed then declare such a task in the Jira ticket, as it may require DevOps assistance (especially if the old module is also still configured in folio-ansible).

Otherwise raise a pull-request for [platform-complete snapshot](https://github.com/folio-org/platform-complete/tree/snapshot) branch.
The module has probably been sitting in the "install-extras.json" file.

## Deal with outstanding PRs

Address outstanding pull requests, e.g. Close with a comment.

This is also a chance to delete any old merged branches, where developers forgot to [Maintain tidy repositories](/guides/tidy-repository/).

## Add notice section to README

Add a new section to the README with heading `DEPRECATED` to explain what happened.
Add this section after the copyright/license notice, and before the Introduction section.

See an example at [mod-bursar-export](https://github.com/folio-org/mod-bursar-export).

Also adjust the copyright year to match the last actual code commit.

## Adjust the About description

In the top-right panel of its GitHub front page is the "About" Description of the repository. This concise description is shown in various listings of repositories.

Adjust it to prepend a concise deprecation notice to the existing description.

See other examples by using the "Repositories" filter at the FOLIO Organization [Overview](https://github.com/folio-org).
Replace the default text "Find a repository" with "deprecated".

## Archive as read-only

At GitHub use the repository Settings: "Archive this repository -- Mark this repository as archived and read-only".

Review the GitHub [documentation](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories) before proceeding.

This will disable push access and pull requests. It leaves the teams configured, and can be temporarily reversed if needed. This also enables scripts to avoid “archived” repositories.

## Finalise

Add a comment to [FOLIO-1838](https://issues.folio.org/browse/FOLIO-1838).
This is a list of all archived modules.

<div class="folio-spacer-content"></div>
