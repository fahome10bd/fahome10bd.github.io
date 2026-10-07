---
permalink: /
title: "Mohammad Mahmudul Hasan"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am the **Project Lead in the AI Department at [HawarIT Limited](https://www.hawarit.com/)**, where I lead multidisciplinary teams developing AI-driven solutions for large-scale geospatial automation and spatial intelligence. Prior to this, I served as Senior AI Engineer and ML Engineer at HawarIT. I graduated with a B.Sc. in Electrical and Electronic Engineering (EEE) from the **Islamic University of Technology (IUT)** in 2021 with a CGPA of **3.76/4.00 (First Class Honours)**. My undergraduate thesis was on neurophysiological signal analysis: *Quantifying the Locomotive Features in EEG of Impaired Consciousness and Coma with Distinctive Cerebral Rhythms* [[IUT Repository](https://repository.iutoic-dhaka.edu/items/e79be58c-22b4-4817-9329-05b0915d8160)] · [[Thesis PDF]({{ '/files/Mohammad_Mahmudul_Hasan_BSc_Thesis.pdf' | relative_url }})].

My transition from Electrical and Electronic Engineering to Geospatial AI was driven by a core realization: while hardware enables sensors to capture the physical world, intelligent algorithms allow us to understand, reconstruct, and reason about it.

<div class="academic-actions">
  <a href="{{ '/files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf' | relative_url }}" class="btn btn--primary"><strong>Download Academic CV (PDF)</strong></a>
</div>

## Research interests

- **3D spatial intelligence:** Semantic understanding of point clouds and urban scenes, with structured CAD/BIM extraction.
- **Urban reconstruction and digital twins:** Connecting photogrammetry and CityGML with neural rendering, including proposed work on 3D Gaussian Splatting.
- **Geospatial automation and change detection:** Reliable processing of aerial imagery and multi-temporal observations for GIS workflows.

[Explore my research directions]({{ '/research/' | relative_url }})

## Selected projects

{% assign project_order = site.portfolio | sort: 'order' %}
{% assign featured_count = 0 %}
{% for item in project_order %}
  {% assign project = site.data.projects[item.content_key] %}
  {% if project.featured and featured_count < 3 %}
<div class="selected-project">
  <h3><a href="{{ item.url | relative_url }}">{{ project.title | escape }}</a></h3>
  <p>{{ project.summary | escape }}</p>
</div>
    {% assign featured_count = featured_count | plus: 1 %}
  {% endif %}
{% endfor %}

[See all projects]({{ '/portfolio/' | relative_url }})

## Peer-reviewed publication

Tasnim Sakib Apon, **Mohammad Mahmudul Hasan**, Abrar Islam, and Md. Golam Rabiul Alam. “Demystifying Deep Learning Models for Retinal OCT Disease Classification using Explainable AI.” *IEEE CSDE, 2021*.

[Publication details]({{ '/publication/retinal-oct-explainable-ai/' | relative_url }}) · [DOI](https://doi.org/10.1109/CSDE53843.2021.9718400) · [Author preprint](https://arxiv.org/abs/2111.03890)

## Contact

For research discussions and graduate opportunities: [mahmudul18@iut-dhaka.edu](mailto:mahmudul18@iut-dhaka.edu).

[Online CV]({{ '/cv/' | relative_url }}) · [GitHub](https://github.com/fahome10bd) · [LinkedIn](https://www.linkedin.com/in/fahome10bd/)
