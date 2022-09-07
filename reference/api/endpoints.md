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

Each link goes directly to the relevant entry in the tables of the [API documentation](/reference/api/).

**NOTE**: [In development](#further-information). The data file has endpoints for only some modules, until each does a new merge to their mainline branch.

## List of endpoints

{% assign urlApiXref = "/reference/api/" %}
{% assign endpointList = "" | split: ',' %}
{% assign missingList = "" | split: ',' %}
{% assign presentCount = 0 %}

{% for repo in site.data.config-apidocs %}
  {% if repo.endpoints.size > 0 %}
    {% assign presentCount = presentCount | plus: 1 %}
    {% for endpoint in repo.endpoints %}
      {%- capture item -%}
        {{ endpoint.path }}|{{ endpoint.methods }}|{{ repo.name }}|{{ endpoint.apiDescription }}
      {%- endcapture -%}
      {% assign endpointList = endpointList | push: item %}
    {% endfor %}
  {% else %}
    {% assign missingList = missingList | push: repo.name %}
  {% endif %}
{% endfor %}

Listed endpoints count: {{ endpointList.size }}

<table>
  <thead>
    <tr>
      <th title="Endpoint methods"> Methods </th>
      <th title="Endpoint path"> Path </th>
      <th title="API documentation"> API documentation </th>
    </tr>
  </thead>
  <tbody>
{% assign endpointListSorted = endpointList | sort %}
{% for item in endpointListSorted %}
  {% assign pieces = item | split: "|" %}
  {% capture file_name %}{{ pieces[3] | split: "/" | last | replace_first: ".raml", "" | replace_first: ".yaml", ""}}{% endcapture %}
  {% capture anchor %}{{ pieces[2] }}: {{ pieces[3] }}{% endcapture %}
  {% capture href %}{{ urlApiXref }}#{{ pieces[2] }}-{{ file_name }}{% endcapture %}
  {% capture link %}<a href="{{ href }}">{{ anchor }}</a>{% endcapture %}
  <tr>
    <td> {{ pieces[1] }} </td>
    <td> {{ pieces[0] }} </td>
    <td> {{ link }} </td>
  </tr>
{% endfor %}
  </tbody>
</table>

## Further information

The list of endpoints is gathered and published during the CI [generation](/reference/api/#generated-during-ci) of each module's API documentation.
A daily Workflow [assembles](/reference/api/#explain-gather-config) the published lists of endpoints.

This facility was first available 2022-09-06. The endpoints for some modules will be missing until they have a new merge to mainline branch.

Present modules count: {{ presentCount }} \
Missing modules count: {{ missingList.size }}

<div class="folio-spacer-content"></div>
