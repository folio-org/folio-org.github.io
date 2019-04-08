---
layout: page
title: Explain internationalization and localization
titleLeader: "FAQ |"
menuTopTitle: Guides
categories: development-tips
faqOrder: 3
---

The [translations](/guides/commence-a-module/#front-end-translations) section of the "Commence a module" guide explains the setup for a new front-end module.

That leads to the [i18n best practices](https://github.com/folio-org/stripes/blob/master/doc/i18n.md) documentation to explain the translation process.

The Wiki page [How To translate FOLIO](https://wiki.folio.org/display/I18N/How+To+translate+FOLIO) has some additional notes.

The FAQ for [dates and times](/faqs/explain-dates-times/) explains the storage and display.

Note: When using the hosted testing environments, please avoid changing the locale of the entire tenant (in the "Settings -> Organization -> Language and localization" menu at the `/settings/organization/locale` URL path).
Changes here affect all users that are performing tests on the hosted testing environments.
There is a temporary, session-based locale switch in the developer settings ("Settings -> Developer -> Session locale" at the `/settings/developer/locale` path).
