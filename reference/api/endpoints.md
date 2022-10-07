---
layout: page
title: API documentation endpoints
permalink: /reference/api/endpoints/
menuInclude: yes
menuLink: yes
menuTopTitle: Reference
menuSubTitle: API endpoints
menuSubIndex: 3
---

## Introduction

This API documentation is automatically [generated](#gathered-lists) from each repository's API description files.

Use the web browser "Find in page" facility.

Each link in the "API documentation" column goes directly to the relevant entry in the tables of the [API documentation](/reference/api/).
Each link in the "Methods" column goes directly to that section of the relevant API documentation.
Sortable via click the column header (default is sorted by Path).
See [Further information](#further-information).

**NOTE**: [In development](#further-information). The data file has endpoints for only some modules, until each does a new merge to their mainline branch.

## List of endpoints

{% assign urlApiXref = "/reference/api/" %}
{% assign urlS3Base = "https://s3.amazonaws.com/foliodocs/api/" %}
{% assign moduleList = "" | split: ',' %}
{% assign modulesMissingMethod = "" | split: ',' %}
{% assign moduleCount = 0 %}

{% for repo in site.data.config-apidocs -%}
  {% assign moduleCount = moduleCount | plus: 1 %}
{% endfor %}

Listed endpoints count: {{ site.data.config-api-endpoints.size }}
-- about 1200 are [expected](#status-of-missing-modules) eventually.

<table class="sortable asc">
  <thead>
    <tr>
      <th title="Endpoint methods" class="no-sort"> Methods </th>
      <th id="ep-path" title="Endpoint path"> Path </th>
      <th id="api-doc" title="API documentation"> API documentation </th>
    </tr>
  </thead>
  <tbody>
{% for item in site.data.config-api-endpoints -%}
  {% assign moduleList = moduleList | push: item.name %}
  {% assign methods = item.methods | split: ' ' -%}
  {% capture file_name %}{{ item.apiDescription | split: "/" | last | replace_first: ".raml", "" | replace_first: ".yaml", "" | replace_first: ".yml", "" }}{% endcapture -%}
  {% assign directory = "s" -%}
  {% if item.apiType == "raml" %}
    {% assign directory = "p" %}
  {% endif %}
  {% capture anchor %}{{ item.name }}: {{ item.apiDescription }}{% endcapture -%}
  {% capture href %}{{ urlApiXref }}#{{ item.name }}-{{ file_name }}{% endcapture -%}
  {% capture link %}<a href="{{ href }}">{{ anchor }}</a>{% endcapture -%}
  {%- capture method_links -%}
    {% for method in methods -%}
      {% assign method_parts = method | split: ':' -%}
      {% if method_parts[1] != "null" %}
        <a href="{{ urlS3Base }}{{ item.name }}/{{ directory }}/{{ file_name }}.html#{{ method_parts[1] }}">{{ method_parts[0] }}</a>
      {% else %}
        {%- assign modulesMissingMethod = modulesMissingMethod | push: item.name %}
        {{ method_parts[0] }}
      {% endif -%}
    {% endfor %}
  {%- endcapture -%}
  <tr>
    <td> {{ method_links }} </td>
    <td> {{ item.path }} </td>
    <td> {{ link }} </td>
  </tr>
{% endfor %}
  </tbody>
</table>
<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable/sortable.min.js"></script>
<script>
  window.addEventListener('load', function () {
    const el = document.getElementById('ep-path')
    if (el) {
      el.click()
    }
  })
</script>

## Further information

### Gathered lists

The list of endpoints is gathered and published during the CI [generation](/reference/api/#generated-during-ci) of each module's API documentation, when there is a merge to their mainline branch.
A daily Workflow [assembles](/reference/api/#explain-gather-config) the published lists of endpoints.

### Some missing links

For some OpenAPI-based modules, there might be missing links in the "Methods" column.
That is because their API description has omitted the "`operationId`" property for that method.

{{ modulesMissingMethod | uniq | join: ", " }}

### Further development

Intend to add a column with information about which "interface".

### Status of missing modules

This facility was first available 2022-09-06. The endpoints for some modules will be missing until they have a new merge to their mainline branch.

{% assign presentCount = moduleList | uniq | size %}
{% assign missingCount = moduleCount | minus: presentCount | minus: 3 %}
Present modules count: {{ presentCount }} \
Missing modules count: {{ missingCount }}

<div class="folio-spacer-content"></div>
