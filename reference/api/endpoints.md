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

This API documentation is automatically [generated](#further-information) from each repository's API description files.

Use the web browser "Find in page" facility.

Each link in the "API documentation" column goes directly to the relevant entry in the tables of the [API documentation](/reference/api/).
Each link in the "Methods" column goes directly to that section of the relevant API documentation.
See [Further information](#further-information).

**NOTE**: [In development](#further-information). The data file has endpoints for only some modules, until each does a new merge to their mainline branch.

## List of endpoints

{% assign urlApiXref = "/reference/api/" %}
{% assign urlS3Base = "https://s3.amazonaws.com/foliodocs/api/" %}
{% assign moduleList = "" | split: ',' %}
{% assign moduleCount = 0 %}

{% for repo in site.data.config-apidocs -%}
  {% assign moduleCount = moduleCount | plus: 1 %}
{% endfor %}

Listed endpoints count: {{ site.data.config-api-endpoints.size }}

<table>
  <thead>
    <tr>
      <th title="Endpoint methods"> Methods </th>
      <th title="Endpoint path"> Path </th>
      <th title="API documentation"> API documentation </th>
    </tr>
  </thead>
  <tbody>
{% for item in site.data.config-api-endpoints -%}
  {% assign moduleList = moduleList | push: item.name %}
  {% assign methods = item.methods | split: ' ' -%}
  {% capture file_name %}{{ item.apiDescription | split: "/" | last | replace_first: ".raml", "" | replace_first: ".yaml", ""}}{% endcapture -%}
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

## Further information

The list of endpoints is gathered and published during the CI [generation](/reference/api/#generated-during-ci) of each module's API documentation.
A daily Workflow [assembles](/reference/api/#explain-gather-config) the published lists of endpoints.

This facility was first available 2022-09-06. The endpoints for some modules will be missing until they have a new merge to their mainline branch.

{% assign presentCount = moduleList | uniq | size %}
{% assign missingCount = moduleCount | minus: presentCount %}
Present modules count: {{ presentCount }} \
Missing modules count: {{ missingCount }}

Links in the "Methods" column were added on 2022-09-10. Links will appear after modules have a new merge to their mainline branch.
For OpenAPI-based modules, if such links are still missing, then that is because the API description has omitted the "`operationId`" property for that method.

<div class="folio-spacer-content"></div>
