---
layout: page
title: How to create a new Tutorial set of documents
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: devdoc
faqOrder: 4
---

To add a new [Tutorial](/tutorials/) to this dev.folio.org site, follow these guidelines.
There are separate guidelines for creating a new [regular document](/faqs/how-to-create-doc/) which also has advice about editing and publishing the changes.

Choose one of the existing tutorials to use as a template, for example the "folio-vm" one.

Create a new git branch, as [explained](/faqs/how-to-create-doc/#about-editing-and-publishing).

Create a new directory:

```
cd tutorials
mkdir my-one
```

Copy the index page of the template tutorial:

```
cp folio-vm/index.md my-one/index.md
```

Edit the page `my-one/index.md` to adjust the YAML front-matter:

* Replace the `title` and adjust the `permalink` to be `/tutorials/my-one/`
* For the `menuSubs` replace the `title` with the short menu title of this tutorial
* For the `menuSubs` replace the `index` with the sequence number to position this new tutorial in the menu structure
* For each `sub` in the `menuSubs` section (i.e. menu items) adjust its `url` to suit (e.g. `/tutorials/my-one/overview/` and `/tutorials/my-one/01-first-lesson/` etc.)
* Adjust the text content of this index page

Copy the overview page of the template tutorial:

```
cp folio-vm/overview.md my-one/overview.md
```

Edit this overview page `my-one/overview.md` to replace the sections for Goals, Prerequisites, etc.
Also adjust its YAML front-matter for its `title` and `permalink` fields.

Edit the page `tutorials/index.md` to add a content link to the new one, as is done for the others.

Add documents for each lesson.

Ensure that the new tutorial can be properly browsed via the local Jekyll server, and that titles and URLs are as expected. Ensure that the new tutorial content can be discovered via local [Search](/search/).

When ready then push the git branch, and create the pull-request as [explained](/faqs/how-to-create-doc/#about-editing-and-publishing).

