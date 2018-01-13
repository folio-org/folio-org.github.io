---
layout: page
title: API documentation
permalink: /doc/api/
menuInclude: yes
menuLink: yes
menuTopTitle: Reference
menuTopIndex: 2
menuSubTitle: "API documentation"
menuSubIndex: 2
---

## Introduction

These API specifications are automatically generated from the relevant
[RAML](https://github.com/folio-org/raml)
files, and specify how client modules may
access the functionality provided by these important core modules.

* view-1: Uses pop-up windows for each method and endpoint.
* view-2: Uses one-page view to everything.

{% assign urlAws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign urlGithub = "https://github.com/folio-org" %}

{% for repo in site.data.api %}
<h2 id="{{ repo[0] }}"> {{ repo[0] }} </h2>
<table class="api">
  <thead>
    <tr>
      <th class="label" title="Label">Label</th>
      <th class="raml" title="APIs and link to RAML source">APIs</th>
      <th class="view" title="View 1: using raml2html">view-1</th>
      <th class="view" title="View 2: using raml-fleece">view-2</th>
    </tr>
  </thead>
  <tbody>
  {%- for docset in repo[1] -%}
    {%- for doc in docset.files -%}
      {% capture urlDoc1 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}.html{% endcapture %}
      {% capture urlDoc2 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}2/{{ doc }}.html{% endcapture %}
      {% capture urlRaml %}{{ urlGithub }}/{{ repo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml{% endcapture %}
    <tr>
      <td> {{ docset.label }} </td>
      <td> <a href="{{ urlRaml }}">{{ doc }}</a> </td>
      <td> <a href="{{ urlDoc1 }}">view-1</a> </td>
      <td> <a href="{{ urlDoc2 }}">view-2</a> </td>
    </tr>
    {%- endfor -%}
  {%- endfor %}
  </tbody>
</table>
{% endfor %}
