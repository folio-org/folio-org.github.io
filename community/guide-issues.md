---
layout: page
title: Guidelines for FOLIO issue tracker
---

[https://issues.folio.org](https://issues.folio.org)

## Sign up for an account

To create issues or add comments, sign up for an account via the front page.
(This is also used to manage accounts for wiki.folio.org)

## Preparing to add an issue

Review the "[which forum](which-forum#issue-tracker)" guidelines
to be sure that adding an issue is the appropriate action.

Describe the issue concisely in the _Summary_ and _Description_ fields.
Use _Comments_ for further detail.
The _Summary_ and _Description_ are also utilized for reports, so detail is
better in _Comments_.

Use the Search facility to ensure that an issue is not already reported.

Use a local text file and your familiar editor to prepare and save the
summary, description, and comments.  When ready then copy-and-paste.

Use attachments for long log files, text listings, and images.
Be sure to redact information that would compromise privacy.

## Create issue

When creating the issue, select the most relevant _Project_ and the _Issue
Type_ (see [below](#issue-types) for definitions).
If unsure which Project, then use "FOLIO".
Someone can change these later if necessary.
For the "Bug" issue type, use the "Configure Fields" option to add
the _Environment_ field.

After issue creation, use
[follow-up _Comments_](#continue) for further detail.
Attachments can be added later.

Someone else will later determine the _Assignee_ and the _Priority_, and will
link between relevant issues.

## Issue types

Each Project uses the following types:

- **New Feature**: Some new functionality request, yet to be developed.
- **Bug**: A defect which impairs or prevents proper function, and
  can usually be resolved without changing the functionality of the system.
- **Task**: Some job that needs to be done, usually not directly related to
  product code changes.
- **Sub-task**: We try to avoid this, and instead use other types,
  and then Link between issues.
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
That is better represented by other means (such as the number of watchers or votes)
and by providing clear Comments about the issue and its impacts.

## Continue

After creating the issue with a concise _Description_, follow up with more
detail in additional _Comments_.

When other people comment and ask for clarification, then try to respond
promptly. We all like to keep the issue resolution process moving smoothly.

If comments start to turn into a lengthy discussion, then follow up in
[other fora](which-forum), and then summarise into further issue tracker Comments.
Provide links in both directions.

## Status

We use the following workflow:

- **Open**: Ready for the assignee to commence work on it.
- **In Progress**: Being actively worked on at the moment by the assignee.
- **Reopened**: The resolution was incorrect, or subsequent developments have caused the issue to resurface.
- **Closed**: Finished.

The Status does not preclude other people from assisting.
Please add relevant Comments.

## Linking

Other people will create tracker Links between relevant issues.

Using an Issue identifier within text Comments will automatically link to
it, e.g. `FOLIO-298`.
Using an issue identifier in git commit messages will also automatically
link to the Issue.

Provide other relevant links, for example GitHub pull requests and
Discuss topics.

## Filters and search

Various issue Filters are available via the "Issues : Search" menu.
For example, the "Added recently"
and "Updated recently" filters help to be aware of recent action.

Create your own filters. Use one as a base, then twiddle and Save As.
