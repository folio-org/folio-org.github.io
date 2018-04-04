---
layout: guidelines
title: Overview
heading: Community Guidelines
permalink: /guidelines/communityguidelines/
---

# Community Guidelines

This section contains guidelines for using the FOLIO community tools and contributing to the FOLIO project.

## Roadmap

The FOLIO wiki contains the [project roadmap](https://wiki.folio.org/display/PC/FOLIO+Roadmap).

## Community Tools

Some of the important forums to collaborate, discuss FOLIO, interact with other participants, and find starting points for documentation.

<table>
  <thead>
    <tr>
      <th>Forum</th>
      <th width="40%">Purpose</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> <a href="https://discuss.folio.org">discuss.folio.org</a> </td>
      <td> The discussion area and mailing lists is via Discuss. </td>
      <td>
        <a href="#discuss">How to</a> |
        Join at front page
      </td>
    </tr>
    <tr>
      <td> <a href="https://wiki.folio.org">wiki.folio.org</a> </td>
      <td>
        Position papers, roadmaps, meeting agendas and minutes, Special Interest Group
        (<a href="https://wiki.folio.org/display/PC/Special+Interest+Groups">SIG</a>) spaces,
        other guidelines.
      </td>
      <td>
        <a href="#wiki">How to</a> |
        Join at front page (same account as Issues)
      </td>
    </tr>
    <tr>
      <td> <a href="https://dev.folio.org">dev.folio.org</a> </td>
      <td> Developer documentation. Also leads to documentation at each repository. </td>
      <td>
        <a href="https://github.com/folio-org/folio-org.github.io/blob/master/README.md">How to</a>
      </td>
    </tr>
    <tr>
      <td> <a href="https://issues.folio.org">issues.folio.org</a> </td>
      <td> The issue tracking and bug tracking system.
      </td>
      <td>
        <a href="#issue-tracker">How to</a> |
        Join at front page |
        <a href="#issue-tracker">Guidelines</a>
      </td>
    </tr>
    <tr>
      <td> <a href="https://github.com/folio-org">github.com/folio-org</a> </td>
      <td> The source-code repositories are via GitHub. </td>
      <td>
        <a href="#github">How to</a> |
        <a href="/source/components/#server-side-1">List of repos</a> |
        <a href="/guidelines/contrib-code/">Contributing</a>
      </td>
    </tr>
    <tr>
      <td> <a href="https://folio-project.slack.com">folio-project.slack.com</a> </td>
      <td> Real-time chat is via Slack. </td>
      <td>
        <a href="#slack">How to</a> |
        <a href="https://slack-invitation.folio.org">Join</a>
      </td>
    </tr>
    <tr>
      <td> </td>
      <td> Other secondary communication channels.</td>
      <td>
        <a href="#secondary">How to</a>
      </td>
    </tr>
  </tbody>
</table>

### Community Representatives

The FOLIO community consists of many significant contributors.  Among
them are community representatives which include:

- Sebastian Hammer, Index Data
- Christopher Spalding, EBSCO
- Michael Winkler, OLE

### Engineering teams

The FOLIO developer community consists of:

- Index Data, which leads the technical development of the FOLIO
  software
- Several software engineering teams
- Contributing developers from the community
- Many supporting individuals whose contributions feed into and guide
  the development process

The following sections list the engineering roles and contacts for the various parts of
the project.  Team members can be contacted via the collaboration tools
listed above.
There is also the [FOLIO Developer Directory](https://wiki.folio.org/display/COMMUNITY/FOLIO+Developer+Directory) listing some developers and their general work areas.

### Engineering core team

The engineering core team sets strategic direction for technical
architecture in the FOLIO software:

- Sebastian Hammer (project lead)
- Nassib Nassar (project lead - technical)
- Jakub Skoczen (technical project manager)
- Adam Dickmeiss
- Vince Bareau
- Peter Murray (community)

### Subproject core teams

Several components of the FOLIO software are distinct subprojects and
have a core team of software engineers with commit-level access to the
source code repositories.  Each subproject generally has a lead
developer who is responsible for selecting new core team members from
the community.

- okapi: Adam Dickmeiss (lead), Heikki Levanto, Jakub Skoczen, John
  Malconian, David Crossley
- mod-auth, mod-users: Kurt Nordstrom (lead)
- mod-metadata: Marc Johnson (lead), Ian Ibbotson, Jakub Skoczen
- mod-circulation, mod-configuration: shale
- raml-module-builder: shale, Adam Dickmeiss, Julian Ladisch
- raml: shale, Adam Dickmeiss
- stripes-core: Niels Erik Nielsen, Jason Skomorowski, Mike Taylor, John Coburn
- stripes-components: John Coburn (lead)
- stripes-connect: Jason Skomorowski, Mike Taylor, Niels Erik Nielsen
- stripes-loader: Jason Skomorowski (lead)
- stripes-sample-platform: Jason Skomorowski (lead)
- okapi-stripes: Wolfram Schneider (lead)
- ui-users: Mike Taylor, Niels Erik Nielsen, Jason Skomorowski, John Coburn, Matt Connolly, Jeremy Huff
- ui-items: Mike Taylor
- ui-okapi-console: Mike Taylor, Niels Erik Nielsen
- cql2pgjson-java: Julian Ladisch (lead)
- container-perf-tests: Adam Dickmeiss (lead), Jakub Skoczen
- folio-sample-modules: Heikki Levanto (lead), Niels Erik Nielsen
- folio-ansible: Wayne Schneider (lead), John Malconian
- folio-org.github.io: David Crossley (lead)

## Contributing to the FOLIO Project

There are many ways to [contribute](#community-guidelines)
to FOLIO development, for example:

- Contributing directly to the software development.
- Engaging with the issue tracker.
- Joining the conversations.
- Participating in Special Interest Groups.

Developers need to efficiently discuss various topics such as issues,
usage quirks, new features, and documentation improvements.
Remember that other developers, the recipients of your messages, are also busy.
They also operate in different time zones. In such busy projects, items can
be easily overlooked, especially when in an inappropriate forum.

We each need to pause and consider the best forum.
There are no rules, but these guidelines can assist.

As explained in the
[collaboration tools](#community-tools) section,
we have four primary forums:
[Discuss](#discuss) (messaging forum),
[Wiki](#wiki) (documents),
[Issues](#issue-tracker) (bug and task tracking), and
[GitHub](#github) (source code and pull requests).

<span id="secondary"/> There are also secondary communication channels, including:
[Slack](#slack) (realtime chat),
[FOLIOForums](https://www.openlibraryenvironment.org/archives/category/olfforum),
conference calls,
Twitter [@folio_lsp](https://twitter.com/folio_lsp),
and in-person meetings.
If something important occurs in a secondary channel, it must be recorded
in a primary channel.

We follow a variation of the Apache motto:
**_If it didn't happen in one of the primary communication channels
(Discuss, Wiki, Issues, and GitHub), it didn't happen._**

## General notes

- See also other notes about
  [FOLIO Communication Spaces](https://wiki.folio.org/display/COMMUNITY/FOLIO+Communication+Spaces).

- Decisions need to be recorded in an appropriate place.
  Sometimes that will be the Issue Tracker, sometimes as Discuss topics,
  sometimes it will be as a position paper on the wiki.

- Use well-chosen words for topic titles and introductory sections.
  This will make it easier to later list and search.

- Make links in each topic, e.g. between an issue tracker item and
  relevant Discuss topics. Our future selves will be thankful when
  we need to explore the reasons for a certain change.
  Note that it is also possible to copy links from the Slack archive.

- Try to search before starting a new topic. If there are duplicates,
  then link them.

- Do not expect immediate answers.

- Try to keep discussion focussed, and as close to the item as possible.
  For example, if your feedback is about a certain GitHub commit, then
  use its comment-on-commit facility.
  Likewise with pull requests and Jira issue tracker.
  
- [Guidelines for Contributing Code](/guidelines/contrib-code):
  GitHub Flow, feature branches, pull requests, version numbers, coding style,
  tests, etc.

- [Which forum](#community-tools) to use for communication:
  Issue tracker, Slack chat, Discuss discussion, GitHub pull requests.
  Some guidelines about when to use each, and some usage tips.

- [Guidelines for FOLIO issue tracker](#issue-tracker).

- Other [guides](/guides/introduction/) and best practices.  

## Discuss

[https://discuss.folio.org](https://discuss.folio.org)

- For asking questions and recording discussions.

- Use the relevant categories.

- For topics that need lengthy or open-ended discussion, this is
  definitely the place.

- If in doubt about which forum to commence a discussion, then using a
  Discuss topic is the best place.

- You might be subsequently asked to explicitly add an Issue Tracker item.
  Link in both directions.

- When seeking input from the broadest reach of FOLIO participants.

- To post or comment, sign up for an account via the front page.

## WIKI

[https://wiki.folio.org](https://wiki.folio.org)

- Position papers, meeting agendas and minutes, special-interest group
  ([SIG](https://wiki.folio.org/display/PC/Special+Interest+Groups)) spaces,
  other guidelines.

- To post or comment, sign up for an account via the front page
  (uses the same account as issues.folio.org).
  
## Issue Tracker

[https://issues.folio.org](https://issues.folio.org)

- Specific bugs, problems, feature requests, obscure messages or behaviour.

- Also tasks that you know need to be done sometime later.

- If not clear whether to add a new issue, then commence a
  Discuss topic or ask via Slack, and later summarize into an Issue.

- Describe the issue concisely in the Summary and Description fields.
  Use Comments for further detail.
  See [Guidelines for FOLIO issue tracker](/guidelines/communityguidelines/#issue-tracker) for notes about what to report and how to do so.

- Follow up in other forums for any lengthy discussion.
  Then summarise into further issue tracker comments.
  Provide links in both directions.

- To create issues or comment, sign up for an account via the front page.

The following guidelines assist with knowing what to report, and how to create and manage issues.

### Signing Up

To create issues or add comments, sign up for an account via the [front page](https://issues.folio.org).
(This is also used to manage accounts for wiki.folio.org, so same account for both.)

### Report various issues

What types of issue does the project want to hear about?

Anything that you find confusing, does not work as expected or as documented,
specific bugs, problems, feature requests, obscure messages or behaviour.
Also tasks that the teams know should be addressed at some time, now or later.

FOLIO aims to provide useful descriptive error messages in the relevant situations.
Please assist that by reporting when a particular message is not fully relevant or could be enhanced.

### Preparing

Review the "[which forum](#community-tools)" guidelines
to be sure that adding an issue is the appropriate action.

Describe the issue concisely in the _Summary_ and _Description_ fields.
Use _Comments_ for further detail.
The _Summary_ and _Description_ are also utilized for reports, so detail is
better in _Comments_.

Use the Search facility to ensure that an issue is not already reported,
or has perhaps resurfaced and so can be further described.

Use a local text file and your familiar editor to prepare and save the
summary, description, and comments.  When ready then copy-and-paste.

Be careful not to speculate too much about the causes of the issue.

Provide the facts, describe your actions, the expected results, and actual results as clearly as possible.
That time spent does help everyone.

Use attachments for long log files, text listings, and images.
Be sure to redact information that would compromise privacy.

### Creating

When creating the issue, select the most relevant _Project_ and the _Issue
Type_ (see [below](#issue-types) for definitions).
Each individual [source code](/source/components) repository's README document has a link to its particular issue tracker Project.
If unsure which Project, then use "FOLIO".
Someone can change these later if necessary.

For the "Bug" issue type, use the "Configure Fields" option to add
the _Environment_ field.

After issue creation, use
[follow-up _Comments_](#comments) for further detail.
Attachments can be added later.

Someone else will later determine the _Assignee_ and the _Priority_, and will
link between relevant issues.

### Issue Types

Each Project uses the following _Issue Types_:

- **New Feature**: Some new functionality request, yet to be developed.
- **Bug**: A defect which impairs or prevents proper function, and
  can usually be resolved without changing the functionality of the system.
- **Task**: Some job that needs to be done, usually not directly related to
  product code changes.
- **Sub-task**: We try to avoid this, and instead use other types,
  and then Link between issues.
- **Umbrella**: This type is used for project management.
  Please use one of the other types.
  
### Priority Levels

The priority level indicates the importance to the dev team.
An Issue Priority is set by the project managers.

- **P1**: highest priority item, drop everything else before this is resolved, reserved for critical bugfixes
- **P2**: high priority level, must be included in the current development cycle
- **P3**: normal priority level, item will be considered for inclusion in the next dev cycle
- **P4**: low priority level, nice-to-have things that require future discussion and design

Note that the priority might not match the severity felt by the issue reporter.
That is better represented by other means (such as the number of watchers or votes)
and by providing clear Comments about the issue and its impacts.

### Comments

After creating the issue with a concise _Description_, follow up with more
detail in additional _Comments_.

When other people comment and ask for clarification, then try to respond
promptly. We all like to keep the issue resolution process moving smoothly.

If comments start to turn into a lengthy discussion, then follow up in
[other forums](#community-tools), and then summarise into further issue tracker Comments.
Provide links in both directions.

### Status

We use the following workflow:

- **Open**: Ready for the assignee to commence work on it.
- **In Progress**: Being actively worked on at the moment by the assignee.
- **Reopened**: The resolution was incorrect, or subsequent developments have caused the issue to resurface.
- **Closed**: Finished.

The Status does not preclude other people from assisting.
Please add relevant Comments.

### Linking

Other people will create tracker Links between relevant issues.

Using an Issue identifier within text Comments will automatically link to
it, e.g. `FOLIO-298`.
Note that it must be upper-case.

Using such an issue identifier in git commit messages will also automatically
link the Issue to the commits.

Provide other relevant links, for example GitHub pull requests and
Discuss topics.

## Filters and search

Various issue Filters are available via the "Issues : Search" menu.
For example, the "Added recently"
and "Updated recently" filters help to be aware of recent action.

Create your own filters. Use one as a base, then twiddle and Save As.

## GitHub

[https://github.com/folio-org](https://github.com/folio-org)

- See the lists of [all repositories](/source/components) with sections for
[server-side](/source/components/#server-side-1) and
[client-side](/source/components/#client-side-1) and
[other](/source/components/#other-projects) projects.

- As explained in
  [Guidelines for Contributing Code](/guidelines/contrib-code),
  use Feature Branches for any task beyond a minor text edit.

- Use a descriptive name for the branch, with an Issue tracker number
  if relevant, e.g. "folio-293-which-forum".

- In the Pull Request, describe your main changes. Also say whether
  it is now ready to merge, or that you are seeking feedback.

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

- Summarize topics out to other forums for better visibility.
  Remember that Slack is a secondary channel: significant ideas and
  decisions must be recorded elsewhere (Discuss, Wiki, Issues or GitHub)
  for broader vetting.

- Follow up on missed topics. This can occur when a flurry happens about
  other topics. Also everyone is busy, and may intend to respond later.
  So pursue topics at a later time or venue.

- A place to get together to solve a particular bug,
  or hold a brainstorming session,
  or to efficiently address a potential mis-understanding.
  Try to choose a time that suits people distributed around the world.

- A place for heads-up type of notices.

- Use some identifying avatar or photo, indicate your timezone, and enhance your profile notes.

- Distinguish different Slack teams using
  [Sidebar Themes](http://slackstyles.com/#/tag/FOLIO):
  "[FOLIO orange](http://slackthemes.net/#/folio_orange)" and
  "[FOLIO purple](http://slackthemes.net/#/folio_purple)".

