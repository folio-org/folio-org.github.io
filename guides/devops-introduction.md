---
layout: page
title: DevOps introduction and resources
permalink: /guides/devops-introduction/
menuInclude: no
menuTopTitle: Guides
---

This is a collection of tips for people assisting with FOLIO development operations.

See also some specific [DevOps Guides](/guides/#development-operations).

## Repositories

These GitHub repositories are utilised for DevOps work.
Some are private, therefore only for people with relevant permissions.

* [jenkins-pipeline-libs](https://github.com/folio-org/jenkins-pipeline-libs)
  -- Shared library for FOLIO Jenkins Pipeline.
  Used for FOLIO continuous integration and continuous deployment (CI/CD) by each project repositories.

* [folio-ansible](https://github.com/folio-org/folio-ansible)
  -- Sample Ansible playbook and roles for FOLIO (and Vagrant).

* [folio-infrastructure](https://github.com/folio-org-priv/folio-infrastructure)
  -- Various infrastructure bits related to FOLIO.

* [folio-tools](https://github.com/folio-org/folio-tools)
  -- Various tools and support glue for FOLIO CI.

* [folio-org.github.io](https://github.com/folio-org/folio-org.github.io)
  -- The source-code repository for this "FOLIO Developers" website at [dev.folio.org](/)

## Starting points and tips

These are some of the main starting points to assist with FOLIO DevOps work.
Use the [Search](/search/) facility for more.

Of course we attend to much more than just the following items.

## Collaboration channels

Introduction to the Community and [Collaboration tools](/community/#collaboration-tools).

The main Slack channels:

* **#folio-devops-internal** -- For our group.
* **#folio-devops** -- For the wider community to ask for DevOps assistance.
* **#folio-hosted-reference-envs** -- For requests and trouble with the regularly-built reference environments.
* **#folio-support** and **#development** -- We encourage developers to seek community support here, leaving the #devops channel for specific DevOps issues.
* **#folio-releases** -- For release announcements.

## Infrastructure

Refer to the overview of the [Build, test, and deployment infrastructure](/guides/automation/) and notes about Jenkins, Docker, Nexus, etc.

See [explanation](https://folio-org.atlassian.net/browse/FOLIO-3171?focusedCommentId=197577) of precedence of environment variables and handling via Okapi (DeploymentDescriptor, system-level, LaunchDescriptor) and support for that in folio-ansible roles.

## Reference environments

Explanations of each of the regularly-built [reference environments](/guides/automation/#reference-environments) including the build times and links to the relevant Jenkins jobs.

Refer to the [explanations](/guidelines/release-procedures/#add-to-platforms) about how these environments are constructed, the key branches, and the key files.
(The Kitfox DevOps Team handles the platform-complete master branch and release branches.)

We monitor those "Reference environment" builds, triage problems, and try to direct issues back to developers.

We try to [limit](/guides/automation/#off-schedule-rebuilds) out-of-band requests to manually rebuild these.
Many other people utilise these systems, so try to limit disruption.
See Slack #folio-hosted-reference-envs channel.
People need to ask there and allow time for others to be aware.

To determine the cause of failed builds, search the [Jenkins output logfile](/faqs/how-to-investigate-jenkins-logs/).
Remember that the cause might be in the earlier [Platform hourly build](/guides/automation/#platform-hourly-build) of "Pipeline build-platform-complete-snapshot" etc.

Encourage developers to utilise the [facility](/faqs/how-to-obtain-refenv-logs/) to obtain reference environment module logs, rather than asking us to do it for them.

## Developer scratch environments

Refer to the Kitfox DevOps Team overview of [How to get started with Rancher environment](/faqs/how-to-get-started-with-rancher/) and Helm.

## GitHub and Jenkins access

Developers need access to GitHub repositories and Jenkins.

### GitHub team access

Refer to FAQ [How to request GitHub user or team access](/faqs/how-to-request-github-access/).

Note that we try to steer clear of managing GitHub access for individuals.
Instead allocate access for a whole [Team](https://github.com/orgs/folio-org/teams) to a repository.

When enabling a team, then also add it to the "Security and analysis" section, so that they can see and attend to scanning alerts.

### GitHub new developer

Refer to FAQ [How to request GitHub user or team access](/faqs/how-to-request-github-access/).

### Jenkins access

For consistently named GitHub repositories, then Jenkins access should be automatic (provided that the user is [logged in](/guides/automation/#jenkins)).

If not, then visit the "Manage Jenkins : Manage and Assign Roles" section.

Do the "Manage Roles" first, then "Assign Roles".

The "Manage roles" cannot have multiple patterns, but can handle a broader regex.
Do not add the outer double-quotes.
The "Add" button is way to the right-hand side.

## Jira developer access

Developers can create their own Jira [accounts](/community/#collaboration-tools).

<div class="attention">
Note: FOLIO DevOps can no longer do the below-mentioned tasks. <br/>
Refer them to the Slack channel #folio-atlassian-support
</div>

Occasionally a project manager (see [team matrix](https://folio-org.atlassian.net/wiki/x/kIBP)) will request special access to maintain the "Fix Version/s" settings.

Visit the Jira admin "User management" and filter to find the relevant user.
Add the Group "external-core-collaborators".
(They might also need "ui-project-admins" or "project-admins". TODO: Clarify.)

## Jira add new project

<div class="attention">
Note: FOLIO DevOps can no longer do the below-mentioned tasks. <br/>
Refer them to the Slack channel #folio-atlassian-support
</div>

Project managers will sometimes ask us to add a new Jira Project.
They should provide the name and key.

Visit the Jira [Browse projects](https://issues.folio.org/secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=all) section to ensure that the name and key is sensible.

Via the Jira top navigation "Projects" tab, select "Create project".
At the bottom of the screen, select "Create with shared configuration".

Select "Choose a project" option "Library Apps (LIBAPP)". Then "Next" to add the details.

After project creation, visit the new project. Select "Project settings" at the bottom of the sidebar.
Then select "Details" and add its GitHub URL.

