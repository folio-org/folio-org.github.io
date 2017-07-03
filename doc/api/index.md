---
layout: page
title: API documentation
---

These API specifications are automatically generated from the relevant
[RAML](https://github.com/folio-org/raml)
files, and specify how client modules may
access the functionality provided by these important core modules.

* view-1: Uses pop-up windows for each method and endpoint.
* view-2: Uses one-page view to everything.

{% assign urlAws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign urlGithub= "https://github.com/folio-org" %}

{% capture arrayStr %}
{% for repo in site.data.api %}
  {% assign groupSize = 0 %}
  {% for docset in repo[1] %}
    {% assign groupSize = groupSize | plus: docset.files.size %}
  {% endfor %}
  {{ groupSize }}#
{% endfor %}
{% endcapture %}
{% assign groupSizes = arrayStr | split: "#" %}

<table>
  <thead>
    <tr>
      <th title="Module">Module</th>
      <th title="Label">Label</th>
      <th title="APIs and link to RAML source">APIs</th>
      <th title="View 1: using raml2html">view-1</th>
      <th title="View 2: using raml-fleece">view-2</th>
    </tr>
  </thead>
  <tbody>
  {% for repo in site.data.api %}
    {% capture groupSpan %}{{ groupSizes[forloop.index0] }}{% endcapture %}
    {% assign itemNum = 0 %}
    {% for docset in repo[1] %}
      {% for doc in docset.files %}
        {% assign itemNum = itemNum | plus: 1 %}
        {% capture rowId %}{{ repo[0] }}_{% if docset.label %}{{ docset.label }}{% endif %}_{{ forloop.index }}{% endcapture %}
        {% capture urlDoc1 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}{% endcapture %}
        {% capture urlDoc2 %}{{ urlAws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}2/{{ doc }}{% endcapture %}
        <tr id="{{ rowId }}">
          {% if itemNum == 1 %}
          <td id="{{ repo[0] }}" rowspan="{{ groupSpan }}"> {{ repo[0] }} </td>
          {% endif %}
          <td> {{ docset.label }}</td>
          <td>
            <a href="{{ urlGithub }}/{{ repo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml"> {{ doc }}</a>
          </td>
          <td><a href="{{ urlDoc1 }}.html">view-1</a></td>
          <td><a href="{{ urlDoc2 }}.html">view-2</a></td>
        </tr>
      {% endfor %}
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
