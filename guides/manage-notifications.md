---
layout: page
title: Manage notifications to keep abreast
permalink: /guides/manage-notifications/
menuInclude: no
menuTopTitle: Guides
---

This guide assists to keep abreast of notifications, and especially to keep up-to-date with topics that are directly relevant to us.

## GitHub email with mentions

Use mail filters to partition the GitHub email notifications. Add another mail filter to copy ones that mention you into another special folder.

```
:0 c
* ^List-Id:.*folio-org.github.com
* ^Cc:.*MyUserId
$MAILDIR/folio-github-issues-me/
```

## Jira email with mentions

Use mail filters to partition the Jira email notifications. Add another mail filter to copy ones that mention you into another special folder.

```
:0 c
* ^From:.*folio-issues@issues.folio.org
* ^Subject: \[FOLIO-ISSUES\].* mentioned you on
$MAILDIR/folio-jira-issues-me/
```

Use a Jira filter to send an email notification about recently updated issues that mention you.
Use "Manage FIlters" to create a filter "mention-me-1h" with the following criteria, and then add a Subscription for "Daily every hour" and not when empty:

```
(summary ~ currentUser() OR description ~ currentUser() OR comment ~ currentUser()) AND updatedDate >= -1h
```

Then filter it at the client side:

```
:0
* ^From:.*folio-issues@issues.folio.org
* ^Subject: \[FOLIO-ISSUES\] Subscription
$MAILDIR/folio-jira-issues-me/
```

Some email clients have less powerful filters. These can be assisted by not having spaces in your Jira username, e.g. rather than "`Julius Caesar`" use "`Julius-Caesar`" or some such.

## Other Jira filters

Keep a wide browser window open with a search that excludes specific projects and provides an overview of everything else recently updated. Use "List View". Keep track of the time that you last assessed the list, and adjust the "updated" time period to match that.

```
project not in (LIBAPP, UX, UXPROD, HK) AND updated >= -24h ORDER BY updated DESC
```

The current sprint:

```
labels in (sprint41) AND (project in (FOLIO) OR labels in (core, ci)) ORDER BY assignee ASC, updated DESC
```

