---
layout: page
title: Manage notifications to keep abreast
permalink: /guides/manage-notifications/
menuInclude: no
menuTopTitle: Guides
---

This guide assists to keep abreast of notifications, and especially to keep up-to-date with topics that are directly relevant to us personally.

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

## Jira in-app notifications

Notifications about tickets that are relevant to each user can also be displayed in the web browser.

We use the [Bug Watcher Notifications](https://marketplace.atlassian.com/apps/1210865/bug-watcher-notifications?hosting=server&tab=overview).
That page also leads to their documentation and their issue tracker.

At your Jira "User profile" (at top-right) there are two new options:
* Watches: For your user general preferences configuration.
* Notifications: Opens a dedicated page for detail and management of current notifications.

The notification panel shows in the far top-right.
Setting your preferences from the default "email-only" to "in-app" causes notifications to also be listed here.

Defining your own notification schemes (which over-ride the system scheme) is done per-user on a per-project basis.
To do so, visit each relevant "Project" and use the left-hand sidebar for "Add-ons : Watches".

