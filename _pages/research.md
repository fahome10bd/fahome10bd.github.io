---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

{{ site.data.research.introduction | markdownify }}

<nav class="research-index" aria-label="Research directions">
{% for module in site.data.research.modules %}
  <a href="#{{ module.id | escape }}">{{ module.title | escape }}</a>
{% endfor %}
</nav>

{% for module in site.data.research.modules %}
<section class="research-module" aria-labelledby="{{ module.id | escape }}">
  <h2 id="{{ module.id | escape }}">{{ module.title | escape }}</h2>
  {% if module.summary and module.summary != '' %}<p class="module-summary">{{ module.summary | escape }}</p>{% endif %}
  {% include content-blocks.html blocks=module.blocks %}
</section>
{% endfor %}

<p class="content-next"><a href="{{ '/portfolio/' | relative_url }}">Projects</a> · <a href="{{ '/publications/' | relative_url }}">Publication</a> · <a href="{{ '/cv/' | relative_url }}">Curriculum vitae</a></p>
