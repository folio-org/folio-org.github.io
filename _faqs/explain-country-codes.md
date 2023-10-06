---
layout: page
title: Explain country codes
titleLeader: "FAQ |"
menuTopTitle: FAQs
categories: development-tips
faqOrder: 7
---

FOLIO uses a specific list of codes for countries.

The list is difficult to find, so:

Start at the [Stripes Components](https://github.com/folio-org/stripes-components/blob/master/README.md#links-to-documentation-of-specific-components-and-utilities) README,
and follow to the [CountrySelection](https://github.com/folio-org/stripes-components/tree/master/lib/CountrySelection) component.

Its CountrySelection.js file imports the higher-level [util/countries.js](https://github.com/folio-org/stripes-components/blob/master/util/countries.js)
which has each entry for the two-letter and three-letter alphabetic codes, and the numeric codes.

The [translations/stripes-components/en.json](https://github.com/folio-org/stripes-components/blob/master/translations/stripes-components/en.json) has the default names in English language, and of course there are the other [translations](/faqs/explain-i18n/).
