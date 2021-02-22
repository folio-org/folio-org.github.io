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
access the functionality provided by these modules.
See [usage notes](#usage-notes) below.

* view-1: Uses pop-up windows for each method and endpoint.
* view-2: Uses one-page view to everything.

This list of modules is sorted into functional groups.

{% assign urlAws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign urlGithub = "https://github.com/folio-org" %}
{% assign urlSourceXref = "/source-code/map/" %}
{% assign noteRaml = 'This is the shared RAML repository. Each module uses a certain version of this as their "raml-util" directory.' %}
{% assign moduleIdEntries = "" | split: ',' %}

{% for group in site.data.apigroup %}
  {% assign groupId = group[0] %}
  <h2 id="{{ groupId }}"> {{ group[1].title }} </h2>
  <p> {{ group[1].description }} </p>
  {%- for module in group[1].modules -%}
    {%- assign moduleId = module -%}
    {%- assign hasModuleId = moduleIdEntries | where_exp: "item", "item == moduleId" | size %}
    {%- if hasModuleId > 0 -%}
      {%- assign moduleIdNum = hasModuleId | plus: 1 -%}
      {%- assign moduleId = moduleId | append: "-" | append: moduleIdNum  -%}
    {%- endif -%}
    {%- assign moduleIdEntries = moduleIdEntries | push: module -%}
    <h3 id="{{ moduleId }}"> {{ module }} </h3>
    {% assign theRepo = '' %}
    {% for repo in site.data.api %}
      {% if repo[0] == module %}
        {% assign theRepo = repo %}
        {% break %}
      {% endif %}
    {% endfor %}
{% if theRepo == '' %}<p> No entry for {{ module }} in api.yml </p>{% endif %}
{% if module == 'raml' %}<p>{{ noteRaml }}</p>{% endif %}
{% if module == 'raml' %}
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
        Source {% if theRepo[1][0].shared %} <a href="#usage-notes"> * </a>{% endif %}
      </th>
      <th class="view" title="View 1: using raml2html default"></th>
      <th class="view" title="View 2: using raml2html plain"></th>
    </tr>
  </thead>
  <tbody>
  {%- for docset in theRepo[1] -%}
    {%- for doc in docset.files -%}
      {% capture urlDoc1 %}{{ urlAws }}/{{ theRepo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}.html{% endcapture %}
      {% capture urlDoc2 %}{{ urlAws }}/{{ theRepo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}p/{{ doc }}.html{% endcapture %}
      {% capture view2 %}{% if docset.version1 %}<a href="{{ urlDoc2 }}">view-2</a>{% endif %}{% endcapture %}
      {% if docset.shared %}
        {% capture urlRaml %}{{ urlGithub }}/raml/blob/HEAD/{{ docset.shared }}/{{ doc }}.raml{% endcapture %}
        {% capture rowId %}{{ theRepo[0] }}-{{ docset.label }}-{{ doc }}{% endcapture %}
      {% else %}
        {% capture urlRaml %}{{ urlGithub }}/{{ theRepo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml{% endcapture %}
        {% capture rowId %}{{ theRepo[0] }}-{{ doc }}{% endcapture %}
      {% endif %}
    <tr id="{{ rowId }}">
{% if theRepo[0] == 'raml' %}
      <td> {{ docset.label }} </td>
{% endif %}
      <td> <a href="{{ urlRaml }}">{{ doc }}.raml</a> </td>
      <td class="view"> <a href="{{ urlDoc1 }}">view-1</a> </td>
      <td class="view"> {{ view2 }} </td>
    </tr>
    {%- endfor -%}
  {%- endfor %}
  </tbody>
</table>
{%- assign urlSourceXrefLocal = urlSourceXref | append:"#" | append:moduleId -%}
<p> <a href="{{ urlSourceXrefLocal }}">Documentation</a> for {{ moduleId }}. </p>
  {% endfor %}
{% endfor %}

## Uploaded

This is a temporary list of modules that are recently using the new method to upload additional API documentation that is build-generated (see [FOLIO-3008](https://issues.folio.org/browse/FOLIO-3008) and Jenkinsfile [configuration](/guides/jenkinsfile/)).
Note: This display is not yet automated, so please notify via [FOLIO-3028](https://issues.folio.org/browse/FOLIO-3028) whenever new modules publish such documentation.

{% for repo in site.data.api-uploaded %}
  {%- assign moduleId = repo[0] -%}
<h3 id="{{ moduleId }}"> {{ moduleId }} </h3>
<table class="api">
  <thead>
    <tr>
      <th class="raml" title="APIs and link to source">
        Source
      </th>
      <th class="view" title="View 1"></th>
      <th class="view" title="View 2"></th>
      <th class="view" title="View 3: build-generated"></th>
    </tr>
  </thead>
  <tbody>
    {%- for doc in repo[1].files -%}
      {% capture rowId %}{{ moduleId }}-{{ doc }}{% endcapture %}
      {% capture urlSource %}{{ urlGithub }}/{{ moduleId }}/blob/master/{{ repo[1].directory }}/{{ doc }}.yaml{% endcapture %}
      {% capture urlDoc3 %}{{ urlAws }}/{{ moduleId }}/u/{{ doc }}.html{% endcapture %}
      {% capture view3 %}<a href="{{ urlDoc3 }}">view-3</a>{% endcapture %}
      <tr id="{{ rowId }}">
        <td> <a href="{{ urlSource }}">{{ doc }}.yaml</a> </td>
        <td> &nbsp; </td>
        <td> &nbsp; </td>
        <td> {{ view3 }} </td>
      </tr>
    {%- endfor -%}
  </tbody>
</table>
{% endfor %}

## Further information

### Configuration {#configure-api-docs}

See [explanation](/faqs/how-to-configure-api-doc-generation/) for how to configure the generation of API documentation of each back-end module.

### Usage notes

* The documents are generated by CI for each repository during the "merge to master" phase.
So the documentation relates only to the current master branch.

* Since August 2018 the generated documents are saved for each software version.
So for [mod-inventory-storage](#mod-inventory-storage) amend the URL of the generated documents to add the version number (major.minor), e.g. `mod-inventory-storage/12.5/...`

* For repositories that are still using RAML-0.8 version, the "view-2" presentation is empty because the software that is used to generate that view only supports RAML-1.0 version.

* NOTE: 2018-11-20: The "view-2" using the "plain" theme is available after each module's next merge to master.

* The asterisk `*` denotes that this is a shared set of RAML files.
The generated documents are for this module's current raml-util, but the link to the source RAML file is to the head of the default branch of the shared
"[raml](#raml)" repository.

* Each section of this page can be directly linked to (e.g. [#mod-notes](#mod-notes)).
Similarly each row of a module's RAMLs (e.g. [#mod-notes-types](#mod-notes-types)).

* See assistance for [How to determine which module handles which interface and endpoint](/faqs/how-to-which-module-which-interface-endpoint/).
