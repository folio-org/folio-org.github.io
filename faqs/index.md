---
layout: page
title: Frequently asked questions
permalink: /faqs/
menuTopTitle: Guides
---

{% for type in site.data.faqs %}
## {{ type.title }}
<div>
  {% if type.description %}
    <p> {{ type.description }} </p>
  {% endif %}
</div>
  {% assign faqs = site.faqs | where_exp: "item", "item.categories contains type.name" | sort: "faqOrder" %}
<ul>
  {% for item in faqs %}
    <li>
      <a href="{{ item.url }}">{{ item.title }}</a>
    </li>
  {% endfor %}
</ul>
{% endfor %}
