---
layout: getstarted
title: Frequently Asked Questions
permalink: /getstarted/faqs/
---

# Frequently Asked Questions

{% for type in site.data.faqs %}
## {{ type.title }}
  {% assign faqs = site.getstarted | where_exp: "item", "item.categories contains type.name" | sort: "faqOrder" %}
<ul>
  {% for item in faqs %}
    <li>
      <a href="{{ item.url }}">{{ item.title }}</a>
    </li>
  {% endfor %}
</ul>
{% endfor %}

