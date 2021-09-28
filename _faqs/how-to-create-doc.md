---
layout: page
title: How to create a new document
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: devdoc
faqOrder: 3
---

## Introduction

To add a new document to this dev.folio.org site, follow these guidelines.
There are separate guidelines for creating a [new FAQ](/faqs/how-to-create-doc-faq/) and a [new Tutorial](/faqs/how-to-create-doc-tutorial/).

After understanding how to be set up for [editing and publishing](#about-editing-and-publishing), then move on the [preparation](#preparation) and creation of a new document.

## About editing and publishing

This section has general tips and background understanding.
It will be more productive to be familiar before starting a new document.

Refer to the [README](https://github.com/folio-org/folio-org.github.io) for this git repository (which is the source for this dev.folio.org website). That also has general explanation about how the site operates.
There are also various notes in the "[Work area - management of dev site](https://github.com/folio-org/folio-org.github.io#work-area---management-of-dev-site)".

As is normal, contributors that do not have write access to this repository will [fork](/guidelines/contributing/#fork-github-repository) and branch and send pull-requests.
Others will directly use feature branches (as master branch is protected) and send pull requests.

See how to [configure](/guides/developer-setup/#use-editorconfig-for-consistent-whitespace) your text editor.

It is best to establish your local Jekyll setup as explained in the [README](https://github.com/folio-org/folio-org.github.io).
Creating documentation can be fiddly.
Develop your branch locally.
View via the local Jekyll server.
When ready then push the branch.
As noted in the README, every push to the repository will cause AWS to rebuild your branch, so best to accumulate commits and push a batch.

(It might be possible to make edits via GitHub, but as noted above, any substantial documentation work is best done locally.)

When ready, create the pull-request as normal. After merge, the dev.folio.org site is regenerated and automatically deployed immediately.

## Preparation

Decide the most [appropriate location](/faqs/where-is-developer-documentation-located/) for the documentation.
If it concerns a [specific module](/source-code/map/) then it may be more appropriate to add to that module's local documentation.

If the new documentation is more appropriate at dev.folio.org, then continue here.

First do some background planning.

Do [search](/search/) first. It might be suitable to add another section to an existing document.

Also search the issue tracker, as someone may have already proposed a similar document.
Generally the documentation tickets use the Jira Label [devdoc](https://issues.folio.org/issues/?jql=labels%3Ddevdoc).
Consider adding a new ticket to facilitate your document development, or to suggest others.

Decide the type of document:
[Guidelines](/guidelines/) (various procedures that should/must be followed),
[Guides](/guides/) (assistance with other topics),
[Tutorials](/tutorials/) (each tutorial is a set of related documents),
or [FAQs](/faqs/).

Decide a clear topic for the document.
This will assist with devising a suitable title and [permalink](#copy).

Plan the internal sections of the new document.

## Learn

Learn how to achieve certain features by inspecting behind-the-scenes of other documents.

## Copy

Copy another similar document to the new file. Use a relevant filename, following the established filename convention, and use hyphen-separated words.

Adjust the YAML front-matter. The `permalink` is the URI of the document.
Choose carefully, so as to not break URLs in the future.

Trim the existing content away.

## Table of contents

The table-of-contents (ToC) in the left-hand navigation panel is automatically generated from the html headings found in the content of the page.

The page title is the level-one heading.

The ToC is produced from the second-level headings (i.e. starting with `## Foo bar` in the Markdown content) and third-level headings are within each section as sub-sections.

Use concise and descriptive section heading titles. About 72 characters is the limit. After that the ToC heading will be rendered with an ellipsis. The tool-tip hover will show the full title text.

## Explicit section link anchors

The fragment identifiers for each section heading are automatically generated from the titles of the headings.

If explicit anchors are required (e.g. to make a better link, or to ensure unique IDs) then use section headings of this form: ``## Complex heading {#instead-do-this``}

For example, see the [source](https://raw.githubusercontent.com/folio-org/folio-org.github.io/master/guides/commence-a-module.md) for [this](/guides/commence-a-module/) page.

## Navigation

If the document has internal sections, then the [Table of contents](#table-of-contents) is automatically generated into the left-handle panel.

Above that in the left-hand panel is the menu for navigation of this particular area of the site.

Not every document is explicitly added to this panel.

See examples of other areas to learn how this is achieved.
For example: [Guidelines](/guidelines/) and [Reference](/reference/) and [Tutorials](/tutorials/).
View the front-matter of files in those areas.

Regarding content links: Make links from relevant content of other documents.

Use links that start with `/` e.g. `/reference/api/`

Do not use links that start with `../foo` which will not function.

## Line breaks

If a line-break is required within a content paragraph, then use the html `<br/>` element.

## Verify links

Do [verify](https://github.com/folio-org/folio-org.github.io#link-checker) internal and external links.

## Verify search

Ensure that the new document can be discovered via the local [Search](/search/) system.

See the [notes](https://github.com/folio-org/folio-org.github.io/blob/master/work/maintain-search.md) in the work area.

Also ensure that the content has appropriate search terms.
Try different ways to find it, and add more search terms.

