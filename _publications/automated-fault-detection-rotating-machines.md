---
title: "An Automated Rule-Based Fault Detection Method for Rotating Machines Using Accelerometer Vibration Signal Analysis"
collection: publications
category: papers
year: 2021
date: 2021-04-15
permalink: /publication/automated-fault-detection-rotating-machines/
venue: "Research Manuscript / Technical Report, Department of EEE, Islamic University of Technology (IUT)"
excerpt: "Automated rule-based fault detection framework analyzing multi-domain accelerometer vibration signals to diagnose bearing, gear, and mechanical faults without manual intervention."
---

**Authors:** Fatema Zerin Prottasha and Mohammad Mahmudul Hasan

**Affiliation:** Department of Electrical and Electronic Engineering (EEE), Islamic University of Technology (IUT), Gazipur, Bangladesh

**Documents:**
- [Download Manuscript (Word .docx)]({{ '/files/Automated_Fault_Detection_Rotating_Machines_Paper.docx' | relative_url }})
- [Download Manuscript (Word .doc)]({{ '/files/Automated_Fault_Detection_Rotating_Machines_Paper.doc' | relative_url }})
- [Download Original Technical Report (PDF)]({{ '/files/Automated_Fault_Detection_Method.pdf' | relative_url }})

### Abstract

Although vibration-based condition monitoring is widely adopted for rotating machinery, fault diagnosis conventionally relies on manual spectral inspection by domain experts. This paper proposes an automated, rule-based fault detection framework that identifies mechanical faults directly from accelerometer vibration signals without human intervention. The method compares the vibration profile of a machine under test against a healthy baseline by extracting four key diagnostic features: root-mean-square (RMS) energy ratio, shaft rotational order (×RPM), spectral peak count via fast Fourier transform (FFT), and peak frequency/phase matching indices. An empirical rule base maps these features to classify bearing faults (inner race, outer race, and ball bearing), mechanical anomalies (unbalance and misalignment), and gear defects. Implemented in MATLAB with an intuitive graphical interface, the proposed system automatically declares the fault category and outputs supporting statistical evidence. Experimental validation on a gear fault dataset confirms accurate, autonomous classification (RMS ratio 0.597, peak order 0.2×RPM), demonstrating its efficacy for practical, real-time machine health monitoring.

