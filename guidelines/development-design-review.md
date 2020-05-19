---
layout: page
title: Development, design, and review processes
permalink: /guidelines/development-design-review/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

This section explains the general development, technical design, and review processes.

* [Goals](#goals) and  [Approach](#approach)
* [Development roles](#development-roles)
* [Development process](#development-process)

Other separate documents pertain to:
* [Pull requests checklists](/guidelines/pull-requests-checklists/)
* [Release procedures](/guidelines/release-procedures/)

## Goals

* Support the scaling of FOLIO development
* Allowing most development to be conducted without centralised authority
* Whilst being as consistent as possible across modules and teams
* And balancing the need for expediency with quality

## Approach

* Decentralised collective ownership of core modules across teams
* Increase visibility of design decisions and how those may affect quality or debt
* Provide a mechanism for coordination between development teams and Technical Council on technical debt and architecture topics

## Development roles

In order to scale the design and code review process, FOLIO has established the following technical groups and roles.

### Technical Lead (TL)

Teams should have at least one Technical Lead who is responsible for guiding the technical work conducted within that team. Some teams have specialist leads for back-end and front-end work.

They are the first point of contact for technical design questions or for identification of debt or architecturally significant decisions.

Technical leads are likely members of the Code Owners for multiple modules, in order to help with reviews and expedite urgent changes.

Technical leads are also members of the Technical Design Owners.

They may also be a Lead Maintainer for some modules.

The technical lead from each team is responsible for reviewing pull requests created by their team, regardless of the repository involved.
This duty may be delegated to a qualified member of their team, e.g. a backend/frontend lead.
However, the responsibility ultimately lies with the tech lead.

To help reduce the burden of PR reviews on lead maintainers, the technical leads are responsible for capturing feature level design on the wiki for purposes of knowledge sharing and eliciting early feedback from other tech leads and maintainers.

Technical leads must have a succession plan with sufficient overlap for knowledge transfer.
The onboarding and handoff process for a tech lead's successor must ensure that the new lead understands their responsibilities and duties.
It must also include updating [team documentation](https://wiki.folio.org/display/FOLIJET/Folio+Development+Team+Home)
to reflect new members and any role changes.

### Code Owner (CO)

Code Owners are collectively responsible for technical aspects of a specific area of the project, for example, a module or shared library.

Code Owners are expected to review pull requests as part of their day-to-day work on FOLIO.

Code Owners are made up of Technical Leads and senior developers from multiple teams, including frequent contributors to an area.

Code Owners are defined by a CODEOWNERS file in the GitHub repository for that area.

### Lead Maintainer (LM)

Each GitHub repository should be assigned a Lead Maintainer.
They are responsible for executing the [release procedures](/guidelines/release-procedures/) for that area,
as well as understanding the code and ensuring best practices are followed.

The Lead Maintainer should also be a Code Owner for the repository.

### Technical Design Owners (TDO)

The Technical Design Owners are responsible for guiding consistent technical decisions across areas of the system.

The group is responsible for ensuring design consistency and raising concern about technical debt or architecturally significant decisions with the Technical Council. This includes reviewing technical proposals for new features at the design stage.

This group consists of Technical Leads, selected senior developers and architects. It will meet periodically.

#### Outstanding decisions

* How often should this group meet?
* How to decide on topics for the agenda?
* How should front-end and back-end audiences be managed?

### Technical Council (TC)

The [Technical Council](/reference/glossary/#tc) is responsible for providing technical oversight across the whole of FOLIO.

They are responsible for FOLIO Architectural Blueprint and the RFC process.

## Development process

### Overview

* [Refinement](#refinement)
* [Sprint planning](#sprint-planning)
* [Development starts](#development-starts)
* [Pull request](#pull-request-code-review) issued, reviewed, and merged
* [Design decisions](#design-decisions) may be raised to Technical Design Owners
* [Technical debt](#technical-debt) may be raised to Technical Council
* [Architectural impact](#architectural-impact) may be raised to Technical Council

### Refinement

During refinement a team works with the relevant Product Owners ([PO](/reference/glossary/#po)) to gain an understanding of upcoming work and split up the work into estimated UI and backend issues.

This process should involve some discussion around design and technical issues. Where possible these should be documented on the issue and followed up by the Technical Lead.

### Sprint planning

The team works with the relevant Product Owners to decide on the work that will be attempted during the next sprint.

The selected work should reflect what the team believes is possible within the sprint, including routine activities that team members are responsible for.

### Development starts

A developer picks up an issue during a sprint. The issue is assigned to the developer and marked as in progress.

This is an opportunity to review the scope of the change and raise questions about the intended behaviour and potential technical impact.

If there are unresolved questions from refinement, these should be addressed as soon as possible after the work is picked up.

#### Questions during development

The developer assigned to the work should endeavour to raise any questions that they have about the work, with the relevant Product Owner or Technical Lead, as soon as possible.

Examples of when to do this:
* The desired behaviour seems unclear, contradictory, or inconsistent with existing behaviour
* The current behaviour or implementation does not make sense
* Insufficient guidance has been provided about the API or internal design for a change
* The change might need an architectural decision or generate technical debt

### Pull request code review

* Developer submits a pull request for the module
  * Developers should first verify the changes against the criteria in any [checklist](/guidelines/pull-requests-checklists/) and [definition of done](/reference/glossary/#dod) defined for the module
  * Issue is marked as "In code review"
  * Pull request maintainer is added as first assignee
* Code Owners are automatically invited to review
* Additional specific reviewers should be invited
* Reviewers (Code Owners and anyone else invited to review the change) provide feedback on the pull request
  * Reviewer should add themselves as a subsequent assignee when they start reviewing, to indicate their intention to conduct a review
* Pull request maintainer collaborates with reviewers to address feedback
  * When feedback is addressed, comments should be resolved
  * Click on "Re-request review" if a reviewer that already gave feedback should come back for the latest changes. This is most relevant if the reviewer requested changes and now should approve them.
* At least one approval (from a Code Owner) is needed for authority to merge the pull request (teams may choose to require more)
* Branch is updated with any changes from master
  * This may trigger an additional round of reviews, if the changes for a merge are significant, at the discretion of the Code Owners
* Pull request is merged
* A fix version is assigned to the JIRA issue
* Issue is closed or marked for review by a Product Owner or tester
  * Backend issues that are not testable via the UI are typically closed
  * Other issues should typically be marked as "In review"
* Developer ensures that the master build is successful
* Issues discovered after a PR has been merged will be resolved by the lead maintainer and relevant technical leads during retrospectives and/or out-of-band discussions.

#### Service Level Agreement

It is important that pull requests are reviewed in a timely manner in order to not hold up development work.

Pull requests should have an initial review within 48 hours (this is an initial threshold to experiment). If no reviewer has allocated themselves within that time, the maintainer should contact their technical lead.

If additional review is desired, the maintainer might elicit help via:
* Commenting on the pull request, including the Code Owners team
* Raising the topic on the #pull-requests channel on [Slack](/guidelines/which-forum/#slack)

The group will then try to identify additional reviewers.

#### Outstanding decisions

* Can the stale review dismissal feature be used for when significant changes happen after a review?
* Can the required reviews feature be used to control the minimum number of reviews required to allow a merge (to a protected master branch)?
* How do we notify developers of a pull request about a broken build?
* Should updating a branch to be mergeable be done via merging or rebasing and forcing an update?
* What universal criteria should apply to all pull requests (e.g. summary information, code coverage etc.)
* Additional guidance around related areas, e.g. the contents of pull requests
* What is the expected time frame for reviews to be performed?
* Who performs the review when there are multiple reviewers available? Of course, the more eyes on code the better, but if two reviewers are reviewing the same PR, unbeknownst to each other, while another PR is waiting, that might not be a good thing. Should we "assign" ourselves to the PR to indicate we are reviewing?
* How many reviewers should review a PR? It sounds like at least 1 at this point.
* Should a lack of an approved review prevent a merge?

### Design decisions

Some changes involve design decisions, for example, introducing a new API or significant changes to internal structure.

In order to make FOLIO APIs and modules as consistent as possible, some of these decisions may benefit from input across teams, from the Technical Design Owners.

#### Outstanding decisions

* Criteria for raising design decisions to the Technical Design Owners
* Process for raising and reviewing these decisions
* Criteria for informing the Technical Council

### Technical debt

The Technical Council maintains a list of technical debt within FOLIO. As part of conducting development, a developer or reviewer might identify debt to be addressed in the future.

This debt might already exist or the change might be introducing it.

#### Outstanding decisions

* Guidance for what could be debt
* Should this decision be made via the Technical Design Owners?
* Process for informing the Technical Council of debt

### Architectural impact

Some design decisions might have an architectural impact. This might mean that these are raised with the Technical Council for review and advise.

#### Outstanding decisions

* Guidance for what decisions are considered architectural
* Process for informing the Technical Council, e.g. raising an RFC

<div class="folio-spacer-content"></div>

