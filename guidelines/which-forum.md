---
layout: page
title: Which forum to use for communication
permalink: /guidelines/which-forum/
menuInclude: no
menuTopTitle: Guidelines
---

## Introduction

Developers need to efficiently discuss various topics such as issues,
usage quirks, new features, and documentation improvements.
Remember that other developers, the recipients of your messages, are also busy.
They also operate in different time zones. In such busy projects, items can
be easily overlooked, especially when in an inappropriate forum.

We each need to pause and consider the best forum.
There are no rules, but these guidelines can assist.

As explained in the
[collaboration tools](/community/#collaboration-tools) section,
we have three primary forums:
[Wiki](#wiki) (documents),
[Issues](#issue-tracker) (bug and task tracking), and
[GitHub](#github) (source code and pull requests).

<span id="secondary"/> There are also secondary communication channels, including:
[Slack](#slack) (realtime chat),
[FOLIO Forums](/community/events/),
conference calls,
Twitter [@folio_lsp](https://twitter.com/folio_lsp),
and in-person meetings.
If something important occurs in a secondary channel, it must be recorded
in a primary channel.

We follow a variation of the Apache motto:
**_If it didn't happen in one of the primary communication channels
(Issues, Wiki, and GitHub), it didn't happen._**

## General notes

- See also other notes about
  [FOLIO Communication Spaces](https://wiki.folio.org/display/COMMUNITY/FOLIO+Communication+Spaces).

- Decisions need to be recorded in an appropriate place.
  Sometimes that will be the Issue Tracker,
  sometimes it will be as a position paper on the wiki.

- Use well-chosen words for topic titles and introductory sections.
  This will make it easier to later list and search.

- Make [links](/guidelines/issue-tracker/#linking) in each topic, e.g. between an issue tracker item and
  relevant GitHub events. Our future selves will be thankful when
  we need to explore the reasons for a certain change.
  Note that it is also possible to copy links from the Slack archive.

- Try to search before starting a new topic. If there are duplicates,
  then link them.

- Do not expect immediate answers.

- Try to keep discussion focussed, and as close to the item as possible.
  For example, if your feedback is about a certain GitHub commit, then
  use its comment-on-commit facility.
  Likewise with pull requests and Jira issue tracker.

## Wiki

[https://wiki.folio.org](https://wiki.folio.org)

- Position papers, meeting agendas and minutes, special-interest group
  ([SIG](https://wiki.folio.org/display/PC/Special+Interest+Groups)) spaces,
  other guidelines.

- To post or comment, sign up for an account via the Issue tracker front page.
  (The Wiki uses the same account as issues.folio.org and reset password happens there too.)

- Assistance with Wiki [search](/search-other/#folio-wiki).

## Issue tracker

[https://folio-org.atlassian.net/jira](https://folio-org.atlassian.net/jira)

- Specific bugs, problems, feature requests, obscure messages or behaviour.

- Also tasks that you know need to be done sometime later.

- If not clear whether to add a new issue, then
  ask via Slack, and later summarize into an Issue.

- Describe the issue concisely in the Summary and Description fields.
  Use Comments for further detail.
  See [Guidelines for FOLIO issue tracker](/guidelines/issue-tracker/) for notes about what to report and how to do so.

- Follow up in other forums for any lengthy discussion.
  Then summarise into further issue tracker comments.
  Provide links in both directions.

- To create issues or comment, sign up for an account via the front page.

- Assistance with Jira [search](/search-other/#folio-issue-tracker).

## GitHub

[https://github.com/folio-org](https://github.com/folio-org)

- See the lists of [all repositories](/source-code) with sections for
[server-side](/source-code/#server-side) and
[client-side](/source-code/#client-side) and
[other](/source-code/#other-projects) projects.

- As explained in
  [Guidelines for Contributing Code](/guidelines/contributing/),
  use Feature Branches for any task.

- Use a descriptive name for the branch, with an Issue tracker number
  if relevant, e.g. "FOLIO-293-which-forum".

- In the Pull Request, describe your main changes. Also say whether
  it is now ready to merge, or that you are seeking feedback.
  Follow the guidelines [Development, design, and review processes](/guidelines/development-design-review/).

-  Ensure that the PR title refers to the relevant Jira ticket identifiers as explained in the requirements of [Pull requests checklists](/guidelines/pull-requests-checklists/)
and in the [Guidelines for FOLIO issue tracker](/guidelines/issue-tracker/#linking).

- To seek feedback on your work, use additional comments on your
  Pull Request. If the specific attention of certain people is needed,
  then @mention their names.

- For specific comments on the work of other people, add comments to
  their Pull Requests or in direct response to their Commits (see
  [example](https://github.com/folio-org/okapi/commit/710e201053897609ceb667e0687f830f92f9d006)).

## Slack

[https://folio-project.slack.com](https://folio-project.slack.com)
(join [here](https://slack-invitation.folio.org) first).

- Real-time chat and messaging.

- Use some identifying avatar or photo, indicate your timezone, and enhance your profile notes.
  In such a busy project this assists knowing a little about each other and enables the chat to be more easily followed.

- Summarize topics out to other forums for better visibility.
  Remember that Slack is a secondary channel: significant ideas and
  decisions must be recorded elsewhere (Issues, Wiki, or GitHub)
  for broader vetting.

- Follow up on missed topics. This can occur when a flurry happens about
  other topics. Also everyone is busy, and may intend to respond later.
  So pursue topics at a later time or venue.

- A place to get together to solve a particular bug,
  or hold a brainstorming session,
  or to efficiently address a potential mis-understanding.
  Try to choose a time that suits people distributed around the world.

- A place for heads-up type of notices.

- There are now many channels. Browse the list via the Slack application, to review and join any appropriate ones.
  Some are not public, so you will need to be invited.
  Some relevant channels for developers are:
  - `#folio-support` -- Any topic needing assistance.
  - `#folio-general` -- Community-wide general FOLIO stuff. Use other channels for development topics.
  - `#folio-development` -- The main development area.
  - `#folio-releases` -- Discussion of quarterly release preparation, and announcement of regular module releases.
  - `#pull-requests` -- A place to request reviews on pull requests.
  - `#folio-hosted-reference-envs` -- Issues with the [reference environments](/guides/automation/#software-build-pipeline) automated builds.
  - `#raml-module-builder` -- Specific discussion for RMB development.
  - `#folio-stripes` -- Specific discussion for front-end development.
  - `#folio-devops` -- Assistance with FOLIO infrastructure, requests to add new GitHub Team members, etc.
  - `#folio-rancher-support` (was previously known as `#scratch-environments`) -- Assistance with the team-specific [Rancher developer scratch environments](/faqs/how-to-get-started-with-rancher/).
  - `#folio-ci` -- Notifications from the Jenkins CI. See usage [notes](/guides/navigate-commits/). Mute this channel and visit when needed.

- Use `@mentions` with care. This is especially important on broad channels such as `#folio-general`, as using `@channel` there will send notifications to many thousands of people.

- Distinguish different Slack workspaces using
  Sidebar Themes:
  "[FOLIO orange](https://slackthemes.net/#/folio_orange)" or
  "[FOLIO purple](https://slackthemes.net/#/folio_purple)".

