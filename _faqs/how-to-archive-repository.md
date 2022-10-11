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

Create a Jira ticket for the project of this module, so that everyone can be aware of what happened to the repository.

Certain operations will require Admin access to the repository.
Please complete all tasks that you have sufficient permissions for, then ask at Slack #devops channel.
Better still, ensure that the relevant team that will be doing the work, does have Admin access.

## Ensure not in a Platform

Ensure that this module is not in a Stripes Platform,
i.e. search in the [platform-complete install.json](https://github.com/folio-org/platform-complete/blob/snapshot/install.json) generated file.

Its functionality should have already moved to other modules.
If still present, then verify that no other module depends upon it
(e.g. search the [Registry of ModuleDescriptors](/faqs/how-to-which-module-which-interface-endpoint/#registry-of-moduledescriptors)).

Raise a pull-request for [platform-complete snapshot](https://github.com/folio-org/platform-complete/tree/snapshot) branch.
Refer to the explanation of how the [platforms are constructed](/guidelines/release-procedures/#add-to-platforms) which describes the various branches and the key files and which ones are generated files.

The process will essentially be the reverse of when modules were initially [installed](/faqs/how-to-install-new-module/).
For front-end modules it should be straight-forward.
For back-end modules it could be more complex. If the module was included by virtue of being required by a front-end module, then it would be automatically removed when that module no longer requires it (on the next [hourly platform build](/guides/automation/#install-json)).
However some backend modules were added via the "install-extras.json" file (in the platform snapshot branch) either because they were not ever required by a frontend module, or the frontend was not yet ready and the entry was not removed from that file when the frontend finally was ready.

If the module was part of a previous Flower release, then raise a pull-request for [platform-complete master](https://github.com/folio-org/platform-complete/tree/master) branch (which will form the basis for the upcoming release).
The back-end modules will have an entry in the "install-extras.json" file (yes, its name is an artefact of the process).
The front-end modules will have an entry in the "package.json" and "stripes.config.js" as described via the previous paragraph.

## Remove from reference environments

If a back-end module was included in the "folio-snapshot" [reference environments](/guides/automation/#reference-environments) and Vagrant boxes, then it will also need to be removed from `folio-ansible/group_vars/snapshot` file.
Please [raise](/faqs/how-to-raise-devops-ticket/) a Jira ticket for FOLIO DevOps.

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
