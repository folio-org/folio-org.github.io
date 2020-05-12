---
layout: page
title: How to create a new FAQ document
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: management other
faqOrder: 100
---

To add a new FAQ to this dev.folio.org site, follow these guidelines.
There are separate guidelines for creating a new [regular document](/faqs/how-to-create-doc/) which also has advice about editing and publishing the changes.

Copy an existing file in the [\_faqs](https://github.com/folio-org/folio-org.github.io/tree/master/_faqs) directory.
Follow the established filename convention and titles scheme.

Allocate one or more `categories` in its frontmatter.
These are defined in the file `_data/faqs.yml`

Adjust the `faqOrder` in its frontmatter.
This defines the explicit order of entries within a section of the generated [all FAQs](/faqs/) index page.
If there are multiple entries with the same number, then the sub-order is alphabetic by filename.
A high number (e.g. 100) will ensure that this entry is always at the end of the section.

The list of [all FAQs](/faqs/) is automatically generated.
