---
layout: archive
title: "Research"
show_title: false
permalink: /research/
author_profile: true
---

{{ site.data.research.introduction | markdownify }}

{% assign thesis = site.data.research.thesis %}
{% if thesis %}
<section class="research-thesis" aria-labelledby="undergraduate-thesis">
  <h2 id="undergraduate-thesis">Undergraduate thesis</h2>
  <p><strong>{{ thesis.title | escape }}</strong><br>{{ thesis.institution | escape }} · {{ thesis.year }}</p>
  <p>{{ thesis.summary | escape }}</p>
  <p><a href="{{ thesis.project_url | relative_url }}">Thesis overview</a> · <a href="{{ thesis.repository_url | escape }}">IUT repository</a> · <a href="{{ thesis.pdf_url | relative_url }}">Download thesis PDF</a></p>
</section>
{% endif %}

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
