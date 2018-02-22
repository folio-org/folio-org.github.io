---
layout: page
title: Thanks from the FOLIO Project
permalink: /about/thanks/
---

We appreciate the many individuals and organizations forming the [community](/community) that contributes to FOLIO.
We also thank the many other open source projects that we depend upon.

## Participating organizations

These are some of the participating organizations.
There is also the [FOLIO Developer Directory](https://wiki.folio.org/display/COMMUNITY/FOLIO+Developer+Directory) listing some developers and their general work areas.

<div class="text-centered">
{% assign thanks = site.data.thanks | shuffle %}
{% for item in thanks %}
  <a href="{{ item.url }}" title="{{ item.name }}"><img src="{{ item.image }}" alt="logo" width="{{ item.width }}" height="{{ item.height }}"/></a>
{% endfor %}
</div>

## Supporting Software and Service Attribution

The FOLIO Project is grateful for support from **Atlassian**.
The project uses Atlassian's [Jira](https://www.atlassian.com/software/jira) product to [track issues and tasks](https://issues.folio.org/) as well as Atlassian's [Confluence](https://www.atlassian.com/software/confluence) product for [publishing the work](http://wiki.folio.org/) of the special interest groups.

<a href="https://www.browserstack.com/"><img src="/images/browserstack-logo.svg" alt="BrowserStack logo" width="250" height="50" /></a><br />
The FOLIO Project is grateful for support from **BrowserStack**.
[BrowserStack](https://www.browserstack.com) enables the FOLIO Project front end developers to automate the tests of changes to user interface code across a variety of browsers.
The project also uses BrowserStack to ensure the proper flow of user interface elements around translated strings of various lengths.
