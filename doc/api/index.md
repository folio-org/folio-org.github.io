---
layout: page
title: API documentation
---

These API specifications are automatically generated from the relevant
[RAML](https://github.com/folio-org/raml)
files, and specify how client modules may
access the functionality provided by these important core modules.

{% assign url_aws = "https://s3.amazonaws.com/foliodocs/api" %}

<ul>
  {% for repo in site.data.api %}
    <li id="{{ repo[0] }}"> {{ repo[0] }}:
      <ul>
        {% for doc in repo[1].files %}
          <li>
            <a href="{{ url_aws }}/{{ repo[0] }}/{{ doc }}.html">
              {{ doc }}
            </a>
          </li>
        {% endfor %}
      </ul>
    </li>
  {% endfor %}
</ul>
