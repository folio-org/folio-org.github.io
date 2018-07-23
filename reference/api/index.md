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

These API specifications are [automatically](#configure-api-docs) generated from each repository's
RAML files, and specify how client modules may
access the functionality provided by these important core modules.

* view-1: Uses pop-up windows for each method and endpoint.
* view-2: Uses one-page view to everything.

{% assign urlAws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign urlGithub = "https://github.com/folio-org" %}
{% assign noteRaml = 'This is the shared RAML repository. Refer to the relevant table above, as each module uses a certain version of this as their "raml-util" directory.' %}

{% for repo in site.data.api %}
<h2 id="{{ repo[0] }}"> {{ repo[0] }} </h2>
{% if repo[0] == 'raml' %}<p>{{ noteRaml }}</p>{% endif %}
{% if repo[0] == 'raml' %}
<table class="api apilabel">
  <thead>
    <tr>
      <th class="label" title="Label">Label</th>
{% else %}
<table class="api">
  <thead>
    <tr>
{% endif %}
      <th class="raml" title="APIs and link to RAML source">
        APIs {% if repo[1][0].shared %} <a href="#usage-notes"> * </a>{% endif %}
      </th>
      <th class="view" title="View 1: using raml2html"></th>
      <th class="view" title="View 2: using raml-fleece"></th>
    </tr>
  </thead>
  <tbody>
  {%- for docset in repo[1] -%}
    {%- for doc in docset.files -%}
      {% capture urlDoc1 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}.html{% endcapture %}
      {% capture urlDoc2 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}2/{{ doc }}.html{% endcapture %}
      {% capture view2 %}{% unless docset.version1 %}<a href="{{ urlDoc2 }}">view-2</a>{% endunless %}{% endcapture %}
      {% if docset.shared %}
        {% capture urlRaml %}{{ urlGithub }}/raml/blob/master/{{ docset.shared }}/{{ doc }}.raml{% endcapture %}
      {% else %}
        {% capture urlRaml %}{{ urlGithub }}/{{ repo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml{% endcapture %}
      {% endif %}
    <tr>
{% if repo[0] == 'raml' %}
      <td> {{ docset.label }} </td>
{% endif %}
      <td> <a href="{{ urlRaml }}">{{ doc }}</a> </td>
      <td class="view"> <a href="{{ urlDoc1 }}">view-1</a> </td>
      <td class="view"> {{ view2 }} </td>
    </tr>
    {%- endfor -%}
  {%- endfor %}
  </tbody>
</table>
{% endfor %}

## Configuration {#configure-api-docs}

See [explanation](/faqs/how-to-configure-api-doc-generation/) for how to configure the generation of API documentation of each back-end module.

## Usage notes

`*` denotes that this is a shared set of RAML files.
The generated documents are for this module's current raml-util, but the link to the source RAML file is to the master of the shared
"[raml](#raml)" repository.
