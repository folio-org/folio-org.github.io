---
layout: page
title: Guidelines for FOLIO issue tracker
permalink: /guidelines/issue-tracker/
menuInclude: no
menuTopTitle: Guidelines
---

[https://issues.folio.org](https://issues.folio.org)

The following guidelines assist with knowing what to report, and how to create and manage issues.

## Sign up for an account

To create issue tickets or add comments, sign up for an account via the [front page](https://issues.folio.org).
(This is also used to manage accounts for wiki.folio.org, so same account for both.)

## Report various issues

What types of issue does the project want to hear about?

Anything that you find confusing, does not work as expected or as documented,
specific bugs, problems, feature requests, obscure messages or behaviour.
Also tasks that the teams know should be addressed at some time, now or later.

FOLIO aims to provide useful descriptive error messages in the relevant situations.
Please assist that by reporting when a particular message is not fully relevant or could be enhanced.

## Preparing to add an issue

Review the "[which forum](/guidelines/which-forum#issue-tracker)" guidelines
to be sure that adding an issue is the appropriate action.

Describe the issue concisely in the _Summary_ and _Description_ fields.
Use _Comments_ for further detail.
The _Summary_ and _Description_ are also utilized for reports and for every notification email, so detail is better in _Comments_.

Use the Search facility to ensure that an issue is not already reported,
or has perhaps resurfaced and so can be further described.

Be careful not to speculate too much about the causes of the issue.

Provide the facts, describe your actions, the expected results, and actual results as clearly as possible.
That time spent does help everyone.

Use a local plain text file and your familiar text editor to prepare and save the summary, description, and comments.
This technique also helps to reduce the amount of notifications from minor edits.
When ready then copy-and-paste.

Jira uses a particular markup language for special formatting, and is different to GitHub etc.
There is a link to Jira help via its "Add Comment" screen.

Use attachments for long log files, text listings, and images.
Be sure to redact information that would compromise privacy.

When filing bug reports from Maven and unit test output, always use Maven non-interactive (option `-B,--batch-mode`) to avoid control characters in output.

## Create issue

When creating the issue, select the most relevant _Project_ and the _Issue
Type_ (see [below](#issue-types) for definitions).
Each individual [source code](/source-code) repository README document has a link to its particular issue tracker Project.
If unsure which Project, then use "FOLIO".
Someone can change these later if necessary.

Select the appropriate "Development Team".
If not sure, then just choose one. Other people can re-allocate.

For the "Bug" issue type, use the "Configure Fields" option to add
the _Environment_ field.

After issue creation, use
[follow-up _Comments_](#continue) for further detail.
Attachments can be added later.

Unfortunately Watchers cannot be added on issue creation.
So use the technique of a concise Description when creating, then immediately add Watchers, then follow-up Comments will notify them.
Another workaround is to add people using the "@mention" facility (type "@" then any part of their name).
They can then choose to add themself as a Watcher.

Someone else will later determine the _Assignee_ and the _Priority_ and the _Sprint_ and will
link between relevant issues.

## Issue types

Each Project uses the following _Issue Types_:

- **New Feature**: Some new functionality request, yet to be developed.
- **Bug**: A defect which impairs or prevents proper function, and
  can usually be resolved without changing the functionality of the system.
- **Task**: Some job that needs to be done, usually not directly related to
  product code changes.
- **Sub-task**: We try to avoid this, and instead use other types,
  and then Link between issues. (Note that sub-task tickets cannot be added to Sprints.)
- **Umbrella**: This type is used for project management.
  Please use one of the other types.

## Priority levels

The priority level indicates the importance to the dev team.
An Issue Priority is set by the project managers.

- **P1**: highest priority item, drop everything else before this is resolved, reserved for critical bugfixes
- **P2**: high priority level, must be included in the current development cycle
- **P3**: normal priority level, item will be considered for inclusion in the next dev cycle
- **P4**: low priority level, nice-to-have things that require future discussion and design

Note that the priority might not match the severity felt by the issue reporter.
That is better represented by other means (such as the number of watchers)
and by providing clear Comments about the issue and its impacts.

## Continue

After creating the issue with a concise _Description_, follow up with more
detail in additional _Comments_.

When other people comment and ask for clarification, then try to respond
promptly. We all like to keep the issue resolution process moving smoothly.

If comments start to turn into a lengthy discussion, then follow up in
[other forums](/guidelines/which-forum/), and then summarise into further issue tracker Comments.
Provide links in both directions.

## Status

We generally use the following workflow.
Also refer to each development team's Definition of Done ([DoD](/reference/glossary/#dod)).

- **Draft**: In preparation, e.g. the Description is not yet ready.
- **Open**: Ready for the assignee to commence work on it.
- **In Progress**: Being actively worked on at the moment by the assignee.
- **Reopened**: The resolution was incorrect, or subsequent developments have caused the issue to resurface.
- **Blocked**: Another issue is impeding progress.
- **In Code Review**: Being assessed by development collaborators.
- **In Review**: When appropriate, this indicates readiness for formal review by testers.
- **Closed**: Finished.

(Also refer to [clarification](https://wiki.folio.org/display/PO/JIRA+status) of [Product Owners](/reference/glossary#po) use of the Status field.)

The Status does not preclude other people from assisting.
Please add relevant Comments.

## Linking

Other people will create tracker Links between relevant issues.

Using an Issue identifier within Jira text Comments will automatically link to
it, e.g. `FOLIO-298`. Note that it must be upper-case with no spaces, i.e. include the hyphen.

Using such an issue identifier slug in git commit messages and pull request titles, will also automatically
link the Issue to the commits.
Refer to [Pull requests checklists](/guidelines/pull-requests-checklists) requirements for using Jira ticket identifier slugs in the titles of pull-requests and relevant commit messages.

Note that Jira will automatically scan GitHub to find pull-request titles, branches, and commits that include such properly formed identifiers.
Links are displayed in the "Development" panel on the right-hand side of a Jira ticket.
That automated discovery is not immediate, and can take 60+ minutes.

Provide other relevant bi-directional links, for example GitHub pull requests and
Discuss topics.

## Filters and search

Various issue Filters are available via the "Issues : Search" menu.
For example, the "Added recently"
and "Updated recently" filters help to be aware of recent action.

Create your own filters. Use one as a base, then adjust and Save As.

There are some example filters at [Manage notifications to keep abreast](/guides/manage-notifications/).

<div class="folio-spacer-content"></div>

