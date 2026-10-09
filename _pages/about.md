---
permalink: /
title: "About"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am the **Project Lead in the AI Department at [HawarIT Limited](https://www.hawarit.com/)**, where I lead multidisciplinary teams developing AI systems for large-scale geospatial automation. I have **five years of industrial experience working in research and development**, with a focus on geospatial AI, computer vision, and spatial automation. My work spans orthophoto production, camera pose estimation, building change detection, LiDAR analysis, and 3D city modeling. I combine algorithm development with system design to turn aerial imagery and point clouds into usable maps, structured spatial information, and detailed 3D models.

My academic foundation is in Electrical and Electronic Engineering. I graduated from the **Islamic University of Technology** in 2021 with a **CGPA of 3.76/4.00 and First Class Honours**. My [undergraduate thesis]({{ '/research/#undergraduate-thesis' | relative_url }}) examined EEG signals and cerebral rhythms in impaired consciousness, and I co-authored a [peer-reviewed study]({{ '/publication/retinal-oct-explainable-ai/' | relative_url }}) on explainable deep learning for retinal OCT classification. My interests have since expanded from interpreting physiological signals to understanding and reconstructing physical environments.

Working across geospatial production pipelines has shaped the research questions I want to pursue. Although individual tasks can be automated, manual steps between image assessment, geometric reconstruction, and spatial validation still limit the consistency and scalability of the overall workflow. This motivates my interest in **autonomous GIS systems** that integrate computer vision, photogrammetry, remote sensing, and point cloud intelligence.

My research interests centre on **3D scene understanding, urban digital twins, and spatiotemporal change detection**. I am particularly interested in investigating how neural rendering methods, including 3D Gaussian Splatting, can complement structured CityGML representations for urban reconstruction. Through graduate research, I aim to extend my engineering experience into reliable spatial AI methods for urban monitoring, infrastructure modeling, and disaster assessment.

<p>
  <a href="{{ '/files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf' | relative_url }}"><strong>Download Academic CV (PDF)</strong></a>
</p>

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
