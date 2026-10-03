---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

My research vision centers on **Towards Autonomous GIS: AI-Driven End-to-End Geospatial Data Processing and Spatial Analysis**. Through my engineering leadership and research at HawarIT Limited, I have worked across the entire geospatial pipeline—from raw aerial imagery and mobile LiDAR to GIS web validation and 3D urban reconstruction. 

While individual AI models have advanced specific tasks, modern geospatial production remains largely semi-automated: critical stages such as aerial triangulation, orthophoto quality assessment, seamline optimization, 3D modeling, and spatiotemporal change analysis still rely heavily on manual human intervention. My research objective is to develop a unified, intelligent framework that integrates Computer Vision, 3D Reconstruction, Remote Sensing, and Point Cloud Intelligence to enable scalable, autonomous spatial data processing and digital twin creation.

---

## 1. Orthophoto Pipeline Automation
{: #1-orthophoto-pipeline-automation}

Standard orthophoto workflows require labor-intensive manual review at multiple stages. This module focuses on automating the end-to-end orthophoto production lifecycle:

* **AI-Based Camera Pose Estimation:** Leveraging feature matching, deep tie-point generation, and multi-view geometric constraints to align newly acquired aerial imagery with historical reference orthophotos. My framework achieves **2-pixel alignment accuracy**, reducing manual aerial triangulation (AT) effort by **90%**.
* **Pre- and Post-Processing Quality Assessment (QA):** Designing convolutional and transformer-based image quality models to automatically detect blur, cloud cover, shadow occlusions, and radiometric anomalies prior to AT filtering, achieving **97% detection accuracy**.
* **Intelligent Seamline Generation & Optimization:** Developing spatial optimization algorithms that incorporate multispectral information, contextual land-use boundaries, and AHN point cloud data within PostgreSQL/PostGIS, cutting manual seamline editing by **65%**.
* **True Orthophoto Validation & DEM Refinement:** Deep learning methods for automated Digital Elevation Model (DEM) refinement and geometric distortion verification around bridges, elevated structures, and building edges.

---

## 2. Intelligent 3D Spatial Modeling & Digital Twins
{: #2-intelligent-3d-spatial-modeling--digital-twins}

High-fidelity urban digital twins are critical for smart city planning, infrastructure simulation, and disaster resilience. This module addresses large-scale 3D reconstruction and neural rendering:

* **Autonomous Digital Twins via CityGML & Gaussian Splatting:** Developing automated pipelines that bridge CityGML geometric models with **3D Gaussian Splatting** for real-time, photorealistic urban scene synthesis.
* **Occlusion-Aware Multi-View Texture Projection:** Designing view-selection algorithms that project high-resolution aerial imagery onto 3D building models while handling occlusions and lighting variations, maintaining texture displacement to **less than 3 pixels**.
* **Video-Based Spatial Reconstruction:** Investigating deep structure-from-motion (SfM) and multi-view stereo techniques for dynamic, large-scale urban environment reconstruction from video sequences.

---

## 3. Remote Sensing & Spatiotemporal Change Detection
{: #3-remote-sensing--spatiotemporal-change-detection}

Detecting genuine physical changes across multi-temporal remote sensing observations is complicated by differing sensor angles, atmospheric effects, seasonal vegetation, and shadows:

* **Multi-Temporal Building Change Detection:** Engineering deep learning models to identify new constructions, demolitions, and structural extensions from multi-year orthophoto surveys. Integrated into a GIS-based web validation platform, this system achieves **88% accuracy** and reduces manual visual inspection by **65%**.
* **Multispectral Earth Observation:** Deploying AI solutions on Sentinel satellite imagery for multi-class crop monitoring, water body delineation, and algae bloom detection. This analytics framework secured **2nd place in an international innovation tender**.
* **Disaster Impact Assessment:** Developing automated spatial damage analysis pipelines to rapidly assess post-event infrastructure integrity following natural hazards.

---

## 4. Point Cloud Intelligence & Spatial Understanding
{: #4-point-cloud-intelligence--spatial-understanding}

Extracting actionable semantic and geometric intelligence from dense, unorganized 3D point cloud data:

* **Semantic Segmentation & BIM Extraction:** AI-driven segmentation algorithms for aerial, mobile, and indoor LiDAR datasets. Implemented automated pipe detection and structural property extraction, achieving **95% extraction accuracy** and a **60% reduction in manual processing time**.
* **360° Street-View GeoAI Localization:** Engineered an end-to-end computer vision pipeline using YOLOv5 and custom multi-object tracking to detect and geospatially localize **130 traffic sign classes and 33 street furniture assets** from vehicle-mounted 360° imagery, achieving **>95% detection accuracy and 92% geospatial localization precision**.
* **3D Object Extraction for Digital Twins:** Generating structured CAD/BIM objects directly from raw point clouds to populate digital twin environments with semantic metadata.

---

## Biomedical Signal Processing
{: #biomedical-signal-processing}

Alongside geospatial intelligence, I maintain a strong foundation in physiological signal analysis and interpretable medical AI:

* **Undergraduate Thesis (IUT):** *Quantifying Locomotive Features in EEG of Impaired Consciousness (Coma) with Distinctive Cerebral Rhythms*. Conducted time-series analysis on clinical EEG signals to identify discriminative spectral and temporal features characterizing depths of consciousness and coma states.
* **Explainable Medical Imaging:** Co-authored peer-reviewed research on explainable deep learning models for retinal Optical Coherence Tomography (OCT) disease classification (*IEEE CSDE 2021*), demystifying neural network decision boundaries for clinical validation.

---

[Projects]({{ '/portfolio/' | relative_url }}) · [Publication]({{ '/publications/' | relative_url }}) · [Curriculum Vitae]({{ '/cv/' | relative_url }}) · [Download CV PDF]({{ '/files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf' | relative_url }})
