---
layout: page
title: Demonstrate classic-jekyll-theme
menuInclude: yes
menuLink: yes
menuTopTitle: Theme-demo
menuTopIndex: 100
menuSubTitle: "Overview"
menuSubIndex: 1
---

Using [github.com/Balancingrock/classic-jekyll-theme](https://github.com/Balancingrock/classic-jekyll-theme)
for our branch at
[https://github.com/folio-org/folio-org.github.io/branches](https://github.com/folio-org/folio-org.github.io/branches)

## Some features

### Developer navbar 

Auto-generated.
See front-matter of each doc for menu-item inclusion and positioning. Uses CSS only.

* TODO: How to include menu-items linked to sections of other docs?
* TODO: Perhaps additional feature to include other items via Liquid processing and an `_data/nav.yml` configuration.

### Top banner and navbar

* TODO: Not yet added. Not sure yet if can be achieved utilising current nav features.

### Secondary and tertiary columns, page-specific

[Secondary column](/doc/api).
See `/doc/api/index.md` front-matter.
See `/_includes/column-secondary-doc-api.html` configuration file
(and `_includes/*-column.html` in the theme).
Tertiary column would also be available.
Configuration for extra columns is switched off for all pages, and applied to specific pages via the front-matter.

Columns using [default](columns) content configuration and widgets.

### Content blocks

[Content blocks](content-blocks).
See `/demo-theme-cjt/content-blocks.md` front-matter.
See `_data/cblocks.yml` configuration file.

### Content widgets

* TODO: Not yet investigated.

### Categories navigation menu

* TODO: Not yet investigated.
Auto-generated. Configured via each page front-matter.

## Some general TODO notes

* The `_sass/folio*.scss` files will need tweaking. They are still as-is for the current "minima" theme. Could also be interfering in some places.

* Investigate other theme configuration abilities.

* Fix and enhance footer.

* Investigate the examples that come with the theme. Copy its "pages" directory to see.
