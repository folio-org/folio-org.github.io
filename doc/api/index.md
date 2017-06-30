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

{% assign url_aws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign url_github= "https://github.com/folio-org" %}

{% capture array_str %}
{% for repo in site.data.api %}
  {% assign group_size = 0 %}
  {% for docset in repo[1] %}
    {% assign group_size = group_size | plus: docset.files.size %}
  {% endfor %}
  {{ group_size }}#
{% endfor %}
{% endcapture %}
{% assign group_sizes = array_str | split: "#" %}

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
    {% capture group_span %}{{ group_sizes[forloop.index0] }}{% endcapture %}
    {% assign item_num = 0 %}
    {% for docset in repo[1] %}
      {% capture num_items %}{{ forloop.length }}{% endcapture %}
      {% for doc in docset.files %}
        {% assign item_num = item_num | plus: 1 %}
        {% capture row_id %}{{ repo[0] }}_{% if docset.label %}{{ docset.label }}{% endif %}_{{ forloop.index }}{% endcapture %}
        {% capture url_doc_1 %}{{ url_aws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}{% endcapture %}
        {% capture url_doc_2 %}{{ url_aws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}2/{{ doc }}{% endcapture %}
        <tr id="{{ row_id }}">
          {% if item_num == 1 %}
          <td id="{{ repo[0] }}" rowspan="{{ group_span }}"> {{ repo[0] }} </td>
          {% endif %}
          <td> {{ docset.label }}</td>
          <td>
            <a href="{{ url_github }}/{{ repo[0] }}/blob/master/{{ docset.directory }}/{{ doc }}.raml"> {{ doc }}</a>
          </td>
          <td><a href="{{ url_doc_1 }}.html">view-1</a></td>
          <td><a href="{{ url_doc_2 }}.html">view-2</a></td>
        </tr>
      {% endfor %}
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
