---
layout: page
title: API documentation
permalink: /reference/api/
menuInclude: yes
menuLink: yes
menuTopTitle: Reference
menuSubTitle: API documentation
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
{% assign noteRaml = 'This is the shared RAML. Refer to the relevant table above, as each module uses a certain version of this as their "raml-util" directory.' %}

{% for repo in site.data.api %}
<h2 id="{{ repo[0] }}"> {{ repo[0] }} </h2>
{% if repo[0] == 'raml' %}<p>{{ noteRaml }}</p>{% endif %}
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
      {% capture view2 %}{% unless docset.version1 %}<a href="{{ urlDoc2 }}">view-2</a>{% endunless %}{% endcapture %}
      {% capture urlRaml %}{{ urlGithub }}/{{ repo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml{% endcapture %}
    <tr>
      <td> {{ docset.label }} </td>
      <td> <a href="{{ urlRaml }}">{{ doc }}</a> </td>
      <td> <a href="{{ urlDoc1 }}">view-1</a> </td>
      <td> {{ view2 }} </td>
    </tr>
    {%- endfor -%}
  {%- endfor %}
  </tbody>
</table>
{% endfor %}
