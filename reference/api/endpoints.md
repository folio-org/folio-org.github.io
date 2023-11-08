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

## List of endpoints

{% assign urlApiXref = "/reference/api/" %}
{% assign urlS3Base = "https://s3.amazonaws.com/foliodocs/api/" %}
{% assign moduleList = "" | split: ',' %}
{% assign modulesMissingMethod = "" | split: ',' %}
{% assign reposNoInterface = "okapi,raml,raml-module-builder,folio-spring-base,folio-vertx-lib" | split: ',' %}
{% assign moduleCount = 0 %}

{% for repo in site.data.config-apidocs -%}
  {% assign moduleCount = moduleCount | plus: 1 %}
{% endfor %}

Listed endpoints count: {{ site.data.config-api-endpoints.size }}

<button type="button" data-column="#ep-interface">Show/Hide column "Interface"</button>
  [explain](#interfaces)

<table class="sortable asc">
  <thead>
    <tr>
      <th title="Endpoint methods" class="no-sort"> Methods </th>
      <th id="ep-interface" title="Endpoint interface" class="hidden-column"> Interface </th>
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
  {% assign interface = item.interface | strip %}
  {% if interface == '' %}
    {% if reposNoInterface contains item.name or item.name contains 'edge-' %}
      {% assign interface = "[ not relevant ]" %}
    {% endif %}
  {% endif %}
  <tr>
    <td> {{ method_links }} </td>
    <td class="hidden-column"> {{ interface }} </td>
    <td> {{ item.path }} </td>
    <td> {{ link }} </td>
  </tr>
{% endfor %}
  </tbody>
</table>
<script src="https://cdn.jsdelivr.net/npm/sortable-tablesort@2.4.0/sortable.min.js"></script>
<script>
  window.addEventListener('load', function () {
    const el = document.getElementById('ep-path')
    if (el) {
      el.click()
    }
  })
// https://codereview.stackexchange.com/a/83847
// Flambino 2015-03-11 https://creativecommons.org/licenses/by-sa/3.0/
// global click handler for any element with a "data-column" attribute
$("[data-column]").on("click", function () {
  var button = $(this),                   // the element that was clicked
      header = $(button.data("column")),  // the cell referenced by the button
      table = header.closest("table"),    // the table in which the cell resides
      index = header.index() + 1,         // convert to CSS's 1-based indexing
      selector = "tbody tr td:nth-child(" + index + ")",  // selector for all body cells in the column
      column = table.find(selector).add(header); // all cells in the column

  // toggle the "hidden" class on all the column cells
  column.toggleClass("hidden-column");
});
</script>

## Further information

### Gathered lists

The list of endpoints (also known as "entry-points") is gathered and published during the CI [generation](/reference/api/#generated-during-ci) of each module's API documentation, when there is a merge to their mainline branch.
A daily Workflow [assembles](/reference/api/#explain-gather-config) the published lists of endpoints.

### Some missing links

For some OpenAPI-based modules, there might be missing links in the "Methods" column.
That is because their API description has omitted the "`operationId`" property for that method.

{{ modulesMissingMethod | uniq | join: ", " }}

### Interfaces

When the API documentation is generated (as explained in the above section [Gathered lists](#gathered-lists)) then the module's set of endpoints is extracted from the API model.
The set of "pathPattern" is extracted from its ModuleDescriptor.
If there is a match for the endpoint path, then the "interface" name is recorded.
The correlation is handled via [folio-tools/api-doc](https://github.com/folio-org/folio-tools/blob/master/api-doc/api_doc.py) (search for "interface").

Show the table column "Interface" and sort by that column.
For example, see the set of modules that implement the "`_timer`" interface.

Sort by the column "API Documentation" and see the interfaces for a particular module, e.g. mod-permissions.

<div class="folio-spacer-content"></div>
