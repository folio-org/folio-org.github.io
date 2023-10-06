---
layout: page
title: Frequently asked questions
permalink: /faqs/
menuInclude: yes
menuLink: yes
menuTopTitle: FAQs
menuTopIndex: 6
menuSubTitle: FAQs overview
menuSubIndex: 1
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
<div class="folio-spacer-content"></div>
