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

Additional menu items (i.e. links to page section headings) is configured in `_data/nav-other.yml` and handled via an extension to `_includes/navbanner.html`

### Top FOLIO-wide navbar

The items are configured in `_includes/folio-navbar.html` and included via `_includes/navbanner.html`

### Secondary and tertiary columns, page-specific

[Secondary column](specific-columns).
See `./specific-columns.md` front-matter.
See `/_includes/column-secondary-specific-columns.html` configuration file.
Tertiary column would also be available.
Configuration for extra columns is switched off for all pages, and applied to specific pages via their front-matter.

Columns using [default](columns) content configuration and widgets.
See `./columns.md` front-matter.
See `_includes/*-column.html` in the theme.

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

* Enhance footer.

* Investigate the examples that come with the theme. Copy its "pages" directory to see. To find sources, do `bundle show classic-jekyll-theme`
