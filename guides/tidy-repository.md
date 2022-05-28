---
layout: page
title: Maintain tidy repositories
permalink: /guides/tidy-repository/
menuInclude: no
menuTopTitle: Guides
---

When developers want to participate in a module's development, it is much more enjoyable and efficient when they can easily follow its resources.
This document is a collection of tips to assist.
Please help to make it so.

The [initial setup](/guidelines/create-new-repo/) of its repository would have followed the various guidelines. So they would find the common documentation in the expected places, such as license statements, direct link to this module's Jira issue tracker project, link to the project-wide contribution guidelines, Jenkinsfile, etc.

The repository would also have the general [structure](/guides/commence-a-module/) and configuration.

Review the repository's setup occasionally.

Re-read the module's README and other documentation from time-to-time, and follow its own instructions.

Minimise documentation where possible, for example by linking directly to specific instructions (e.g. to particular [Stripes CLI Commands](https://github.com/folio-org/stripes-cli/blob/master/doc/commands.md) rather than re-explaining.

Run a documentation link verifier occasionally, e.g. [markdown-link-check](https://github.com/tcort/markdown-link-check).

The repository probably has [coding style](/guidelines/contributing/#coding-style) configuration files (`.editorconfig` `.eslintrc`) to partially assist. However some developers might not have text-editors configured, so code style may need to be tidied.
Usually do such changes in a totally separate pull request.

At GitHub keep the "branches" area tidy and prune the unnecessary branches. Of course some may need to remain, but many branches can be deleted after their pull requests have been merged.

Follow-up with [outstanding pull requests](/search-other/#github).

If a repository is no longer maintained, and a decision has been made to archive the repository, then follow FAQ [How to archive a GitHub repository](/faqs/how-to-archive-repository/).
