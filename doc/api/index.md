---
layout: page
title: API documentation
---

These API specifications are automatically generated from the relevant
[RAML](https://github.com/folio-org/raml)
files, and specify how client modules may
access the functionality provided by these important core modules.

{% assign url_aws = "https://s3.amazonaws.com/foliodocs/api" %}
{% assign url_github= "https://github.com/folio-org" %}

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
    {% for docset in repo[1] %}
      {% for doc in docset.files %}
        {% capture str_id %}{{ repo[0] }}_{% if docset.label %}{{ docset.label }}{% endif %}_{{ doc }}{% endcapture %}
        {% capture url_doc_1 %}{{ url_aws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}{{ doc }}{% endcapture %}
        {% capture url_doc_2 %}{{ url_aws }}/{{ repo[0] }}/{% if docset.label %}{{ docset.label }}/{% endif %}2/{{ doc }}{% endcapture %}
        <tr id="{{ str_id }}">
          <td> {{ repo[0] }} </td>
          <td> {{ docset.label }} </td>
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
