---
title: "Orthophoto production, pose estimation, and AI QA"
collection: portfolio
order: 3
permalink: /portfolio/orthophoto-production/
excerpt: "Automated orthophoto production with AI image quality assessment (97%), PostGIS/AHN seamline optimization, and 2-pixel camera pose estimation."
---

At HawarIT Limited, I architected and implemented AI-based automation tools across the photogrammetric orthophoto production lifecycle, eliminating critical manual bottlenecks in image filtering, triangulation, and seamline generation.

### Technical Implementation & Impact
- **AI-Based Image Quality Assessment (QA):** Developed deep learning models to detect cloud, shadow, and blur artifacts on raw aerial imagery prior to aerial triangulation (AT), achieving **97% QA accuracy**.
- **Automated Camera Pose Estimation:** Engineered a feature-matching and tie-point generation framework to register incoming flight images against historical reference orthophotos. Attained **2-pixel alignment accuracy**, cutting manual aerial triangulation effort by **90%**.
- **Seamline Refinement via PostGIS & AHN LiDAR:** Automated seamline placement and geometric validation using PostgreSQL/PostGIS paired with AHN airborne LiDAR elevation data, cutting manual seamline editing by **65%**.

[Research Interests: Orthophoto Pipeline Automation]({{ '/research/#1-orthophoto-pipeline-automation' | relative_url }})
