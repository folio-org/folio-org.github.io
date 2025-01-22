---
layout: page
title: Search dev.folio.org
permalink: /search/
menuInclude: yes
menuLink: yes
menuTopTitle: Search
menuTopIndex: 100
tertiary-column: present
tertiary-column-content: column-2-search.html
---

## Search input

<div id="indexCount"></div>

<div class="form">
  <form action="get" id="searchDev">
    <input type="text" size="25" id="searchInput" autofocus>
    <input type="submit" value="Search">
  </form>
</div>

<div id="hits"></div>

<ul id="searchResults"></ul>

<script src="https://cdn.jsdelivr.net/npm/js-search@2.0.1/dist/umd/js-search.min.js"></script>
<script src="/assets/js/search-dev.js"></script>

## Other information

See [Search other places](/search-other/) for other search and report facilities such as for GitHub, FOLIO Wiki, etc.

