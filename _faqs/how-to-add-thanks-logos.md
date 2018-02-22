---
layout: page
title: How to add logos to the Thanks page
titleLeader: "FAQ |"
menuTopTitle: Documentation
categories: other
faqOrder: 2
---

Gather an appropriate logo image. Trying to keep to around 150x150 dimensions.

Add it to the `/images/thanks-logos/` directory.

Add its entry to the `_data/thanks.yml` configuration file.

The array of images is shuffled every time the site is built for deployment (not on every page view), a small random set is placed on the front page, and the full set is placed on the [thanks](/about/thanks/) page.
