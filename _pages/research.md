---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---

{{ site.data.research.introduction | markdownify }}

<div class="reference-research-grid">
{% for module in site.data.research.modules %}
  {% assign research_path = '/research/' | append: module.id | append: '/' %}
  {% assign cover = module.blocks | where: 'type', 'image' | first %}
  <article class="reference-research-card">
    <h2 id="{{ module.id | escape }}"><a href="{{ research_path | relative_url }}">{{ module.title | escape }}</a></h2>
    {% if cover %}<a href="{{ research_path | relative_url }}"><img src="{{ cover.src | relative_url }}" alt="{{ cover.alt | escape }}" loading="lazy" decoding="async"></a>{% endif %}
    <p>{{ module.summary | escape }}</p>
  </article>
{% endfor %}
</div>
