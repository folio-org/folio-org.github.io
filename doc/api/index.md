---
layout: page
title: API documentation
---

This API documentation is generated from RAML files in each repository:

{% assign url_aws = "http://foliodocs.s3-website-us-east-1.amazonaws.com/api" %}

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
