---
layout: page
title: API documentation
---

This API documentation is generated from RAML files in each repository:

{% assign url_aws = "http://foliodocs.s3-website-us-east-1.amazonaws.com" %}

<ul>
  {% for repo in site.data.api %}
    <li id="{{ repo.name }}"> {{ repo.name }}:
      <ul>
        {% for doc in repo.files %}
          <li>
            <a href="{{ url_aws }}/{{ repo.name }}/{{ doc }}.html">
              {{ doc }}
            </a>
          </li>
        {% endfor %}
      </ul>
    </li>
  {% endfor %}
</ul>
