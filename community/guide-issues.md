---
layout: page
title: Guidelines for FOLIO issue tracker
---

[https://issues.folio.org](https://issues.folio.org)

## Preparing to add an issue

Describe the issue concisely in the _Summary_ and _Description_ fields.
Use _Comments_ for further detail.
The _Summary_ and _Description_ are also utilized for reports, so detail is
better in _Comments_.

Use the Search facility to ensure that an issue is not already reported.

To avoid issues with login timeouts, use a local text file to prepare the summary and description, then copy-and-paste.

Use attachments for long log files, text listings, and images.  
Be sure information that would compromise a user's privacy is redacted from log files.

## Create issue

When creating the issue, select the most relevant _Project_ and the _Issue
Type_ (see [below](#issue-types) for definitions).
If unsure which Project, then use "FOLIO".
If unsure which Type, then use "Task".
Someone can change these later if necessary.
For the "Bug" issue type, use the "Configure Fields" option to add the _Environment_ field.

After issue creation, use follow-up _Comments_ for further detail.
Attachments can be added later.

Someone else will later determine the _Assignee_ and the _Priority_, and will
link between relevant issues.

## Issue types

Each Project uses the following types:

- **New Feature**: Explain something new, yet to be developed.
- **Bug**: A problem which impairs or prevents proper function.
- **Task**: Something else that needs to be done.
- **Umbrella**: This type is used for project management.
  Please use one of the other types.

## Priority levels

The priority level indicates the importance.
An issue's priority is set by the project managers.

- **P1**: highest priority item, drop everything else before this is resolved, reserved for critical bugfixes
- **P2**: normal priority level, must be included in the current development cycle
- **P3**: low priority level, item will be considered for inclusion in the next dev cycle
- **P4**: lowest priority level, nice-to have things that require future discussion and design

## Status

We use the following workflow:

- **Open**: Ready for the assignee to commence work on it.
- **In Progress**: Being actively worked on at the moment by the assignee.
- **Reopened**: The resolution was incorrect.
- **Closed**: Finished.

This Status does not preclude other people from assisting.
Please add relevant Comments.

## Linking

Other people will create tracker Links between relevant issues.

Using an Issue identifier within text Comments will automatically link to
it, e.g. `FOLIO-298`.
Using an issue identifier in git commit messages will also automatically link to the Issue.

Provide other relevant links, for example GitHub pull requests and
Discuss topics.

## Filters

Various issue Filters are provided. For example, the "Added recently"
and "Updated recently" filters help to be aware of recent action.

Create your own filters. Use one as a base, then twiddle and Save As.
