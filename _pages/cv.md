---
layout: single
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% assign cv = site.data.cv %}
<div class="moderncv-container">
  <div class="mcv-download-bar"><a class="btn btn--primary" href="{{ '/files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf' | relative_url }}">Download academic CV (PDF)</a></div>
  <div class="mcv-header">
    <div><span class="mcv-first-name">{{ cv.first_name | escape }}</span><span class="mcv-last-name">{{ cv.last_name | escape }}</span><div class="mcv-subtitle">{{ cv.subtitle | escape }}</div></div>
    <div class="mcv-contact-block">
    {% for contact in cv.contact %}
      {% if contact.url != '' %}<a href="{{ contact.url | escape }}">{{ contact.text | escape }}</a>{% else %}{{ contact.text | escape }}{% endif %}<br>
    {% endfor %}
    </div>
  </div>
  {% for section in cv.sections %}
  <section>
    <div class="mcv-section-heading"><h2 class="mcv-section-title">{{ section.title | escape }}</h2><span class="mcv-section-rule" aria-hidden="true"></span></div>
    {% for row in section.rows %}
    <div class="mcv-entry"><div class="mcv-entry-left">{{ row.label | escape }}</div><div class="mcv-entry-right">{{ row.body }}</div></div>
    {% endfor %}
  </section>
  {% endfor %}
  <section>
    <div class="mcv-section-heading"><h2 class="mcv-section-title">References</h2><span class="mcv-section-rule" aria-hidden="true"></span></div>
    <div class="mcv-ref-grid">
    {% for reference in cv.references %}<p><strong>{{ reference.name | escape }}</strong><br>{{ reference.title | escape }}<br>{{ reference.organization | escape }}<br><a href="mailto:{{ reference.email | escape }}">{{ reference.email | escape }}</a></p>{% endfor %}
    </div>
  </section>
</div>
