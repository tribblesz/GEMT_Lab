---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/3D Analysis of Advanced Nano-Devices Using Electron and Atom Probe Tomography.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# 3D Analysis of Advanced Nano-Devices Using Electron and Atom Probe Tomography

## Source PDF

[[Resources/APT-FIM/PDFs/3D Analysis of Advanced Nano-Devices Using Electron and Atom Probe Tomography.pdf]]

## Overview
The study focuses on the 3D characterization of complex semiconductor architectures, specifically Gate-All-Around (GAA) and tri-gate Si nanowire transistors. The research employs a correlative microscopy workflow, combining Electron Tomography (ET) via STEM-HAADF and Atom Probe Tomography (APT) on the same needle-shaped specimen tips to achieve full 3D morphological and chemical quantification.

## Key Findings
* **Synergistic Reconstruction:** Integrating ET with APT allows for an "atomic density correction" workflow. ET data provides dimensional/morphological benchmarks used to rectify APT dimensional distortions, improving reconstruction accuracy without altering local chemical composition.
* **APT vs. STEM Capabilities:** While STEM-HAADF is effective for morphology and $Z$-contrast-based dimensional variation, it cannot provide absolute chemical identification or distinguish the $SiO_x$ interlayer from the Si channel. Conversely, APT provides essential 3D mapping of atomic chemical distributions and can successfully discriminate between these layers.
* **Identification of Artifacts:** Disparate evaporation fields between materials (e.g., Si vs. dielectrics) cause "local magnification effects." This leads to significant reconstruction distortions, including lateral compression of the Si core, "S-shape" deformations, and overestimation of Si nanowire core density.
* **Chemical Robustness:** Notably, while these structural/geometric artifacts affect dimensional accuracy, they do not impact the accuracy of chemical identification.

## Methods And Instrumentation Notes
* **Instrumentation:** Experiments utilized a CAMECA LAWATAP with an amplified Ytterbium-doped laser ($\lambda$ = 343 nm). Parameters: pulse energy 35 nJ, pulse duration 350 fs, 100 kHz repetition rate, and 300 nm spot size.
* **Sample Preparation:** Needle-shaped specimens were prepared via Gallium Focused Ion Beam (Ga-FIB). A low-energy (2 keV) beam was used during the final annular milling stage to minimize ion irradiation damage on tip sidewalls.
* **Numerical Modeling:** 3D simulations modeled field evaporation ($F_{ev} = V / (\beta R)$) across heterogeneous layers, accounting for specific evaporation fields: $Si$, $TiN$ (38 V/nm), $SiO_2$ (43 V/nm), and $HfO_2$ (51 V/nm).
* **Analytical Challenges:** 
    * **Mass Overlap:** Severe mass-to-charge ratio overlaps in the $TiN/HfO_2/SiO_2$ stack (e.g., $Ti^{3+}$ with $O_2^{2+}$; $N^+$ with $Si^{2+}$) require fine-scale mass spectrum analysis.
    * **Sampling Volume:** Small sampling volumes (0.1 nm) increase concentration errors and may introduce artificial intermixing artifacts due to local magnification.

## Relevance To APT/FIM
* **Dopant Mapping:** Laser-assisted evaporation enables direct 3D mapping of dopant distributions (e.g., B, As, P) in MOSFETs and FinFETs.
* **Interface Analysis:** APT is critical for calculating concentration profiles across essential interfaces, such as the transition from Si channels to $TiN$ gates.
* **Methodological Refinement:** The study highlights the necessity of advanced reconstruction algorithms that incorporate density corrections to mitigate local magnification errors caused by varying evaporation fields.

## Open Questions
* **Evaporation Dynamics:** There is a significant technical gap regarding the precise knowledge of evaporation dynamics for various species under laser pulses.
* **Laser Response:** A deeper understanding is required regarding how different chemical species within multi-material devices specifically respond to laser-assisted evaporation.

## Citation Trail

- pages 1-2: **Summary: 3D Analysis of GAA and Tri-gate Si Nanowire Transistors**

* **Methodology:** The study employs a dual-technique approach, combining Electron Tomography (ET) and Atom Probe Tomography (APT) to achieve full 3D characterization of the morphology and chemical composition of gate-all-around (GAA) and tri-gate Si nanowire transistors.
* **Electron Tomography (STEM-HAADF):** Utilizing STEM with a High-Angle Annular Dark-Field (HAADF) detector, ET is effective for determining device morphology and dimensional variations via $Z$-contrast; however, it lacks the ability to provide absolute chemical identification. Spatial resolution ranges from 2–5 nm but can approach atomic resolution in very small samples if crystallographic orientations are known.
* **APT Limitations:** While APT provides essential 3D mapping of atomic chemical distributions, the reconstructed volumes suffer from significant dimensional distortions.
* **Synergistic Reconstruction:** The integration of both techniques allows for a "correction" workflow: ET data can be used to implement an atomic density correction method to rectify APT dimensional distortions and provide better insight into field evaporation mechanisms, ultimately improving reconstruction accuracy.
- pages 2-3: **Lab Notebook Summary: 3D Analysis of Nano-Devices (APT/TEM)**

* **APT Capabilities & Relevance:** Atom Probe Tomography (APT) provides quantitative 3D chemical mapping at the atomic scale with a field of view (FOV) up to 150 nm. The development of laser-assisted evaporation enables the direct mapping of dopant distributions (e.g., B, As, P) in semiconductor architectures like MOSFETs and FinFETs.
* **Instrumentation Details:** APT experiments were performed using a CAMECA LAWATAP equipped with an amplified Ytterbium-doped laser ($\lambda$ = 343 nm). Key parameters included a pulse energy of 35 nJ, pulse duration of 350 fs, a 100 kHz repetition rate, and a 300 nm spot size.
* **Sample Preparation Method:** Needle-shaped specimens were prepared via Gallium Focused Ion Beam (Ga-FIB). To minimize ion irradiation damage on the tip sidewalls, a low-energy (2 keV) beam was used during the final annular milling stage.
* **Critical Caveats & Artifacts:** Reconstruction accuracy is limited by varying evaporation fields between different materials within a single 3D structure. This leads to significant artifacts, including distorted interfaces and incorrect local composition measurements caused by ion trajectory overlaps.
- pages 3-4: **Lab Notebook Summary: 3D Analysis of GAA and Tri-gate Transistors**

* **Methodology & Instrumentation:** 3D Atom Probe Tomography (APT) was performed on GAA and tri-gate structures using a basic shank angle reconstruction algorithm. A top-down geometry was employed to enhance depth resolution, with chemical species identified via time-of-flight mass spectrometry.
* **Comparative Advantage over STEM:** While STEM HAADF tomography provides large FOV morphology, it lacks the Z-contrast necessary to distinguish the $SiO_x$ interlayer from the Si channel and cannot provide composition quantification. In contrast, APT successfully discriminates the $SiO_2$ interlayer from the Si channel and provides full chemical identification.
* **Morphological Artifacts:** APT reconstructions exhibit significant deviations from electron tomography, specifically lateral compression of the Si core and "S-shape" deformations related to the feature's distance from the tip axis. These distortions lead to inaccurate measurements of device dimensions/shape if taken directly from the reconstructed volume.
* **Physical Origin of Distortions:** The observed artifacts are attributed to the local magnification effect caused by disparate evaporation fields (the Si nanowire has a lower evaporation field than the surrounding dielectrics). This causes ion trajectories to focus, artificially enhancing measured atomic density; notably, however, these structural artifacts do not affect the accuracy of chemical identification.
- pages 4-5: **Lab Notebook Summary: APT Reconstruction Artifacts in Nanowire Transistors**

* **Key Caveat:** APT reconstructions of GAA and tri-gate silicon nanowire transistors exhibit significant distortions when compared to electron tomography; specifically, these artifacts lead to an overestimation of the Si nanowire core density and inaccurate dimensional measurements.
* **Methodology:** To investigate the origin of these distortions, 3D numerical simulations were performed to model the atom evaporation process across the heterogeneous layers of the transistor structure.
* **Instrumentation Physics:** The simulation relies on the relationship for the critical evaporation field ($F_{ev}$), defined as $F_{ev} = V / (\beta R)$, where $V$ is the applied voltage, $R$ is the tip radius, and $\beta$ is a quasi-constant geometric factor.
* **Simulation Parameters:** The model simulates field evaporation by treating surface atoms as metallic cells being removed under an electric field, specifically accounting for the different evaporation fields required for each distinct material layer in the device.
- pages 5-6: **Lab Notebook Summary: 3D Analysis of GAA/Tri-gate Transistors via APT/TEM**

* **Simulation Methodology:** The study utilizes a numerical field evaporation model to simulate the evolution of tip shape and ion trajectories in Gate-All-Around (GAA) structures. The model calculates electric fields at surface atoms, removing those with the highest field and recalculating electrostatic potential to track how different material evaporation fields—specifically $Si$, $TiN$ (38 V/nm), $SiO_2$ (43 V/nm), and $HfO_2$ (51 V/nm)—drive tip morphology.
* **Geometric Artifacts & Magnification:** Discrepancies in evaporation fields between the Si nanowire and surrounding oxides cause significant local magnification effects. High positive curvature in protruding oxides increases magnification, while the Si nanowire surface exhibits flat or negative curvature, leading to trajectory compression and characteristic 3D reconstruction distortions (e.g., compressed square channels).
* **Reconstruction Refinement:** To improve APT accuracy, density corrections were applied using average dimensions obtained from electron tomography. This procedure corrected local atomic density without altering local composition, resulting in a much higher correlation between APT-reconstructed shapes and TEM/STEM measurements.
* **Analytical Caveats & Mass Overlap:** Quantitative analysis is heavily complicated by severe mass-to-charge ratio overlaps in the $TiN/HfO_2/SiO_2$ stack (e.g., $Ti^{3+}$ with $O_2^{2+}$; $N^+$ with $Si^{2+}$), requiring fine-scale mass spectrum analysis and isotopic ratio estimation. Additionally, while small sampling volumes (0.1 nm) enhance sensitivity to interface roughness, they increase concentration errors by several percent and may introduce artificial intermixing artifacts due to local magnification.
- pages 6-7: **Lab Notebook Summary: 3D Analysis of Advanced Nano-Devices (Grenier et al.)**

* **Complementary Analytical Approach:** The study demonstrates that combining Electron Tomography (ET) and Atom Probe Tomography (APT) is essential for analyzing complex architectures (e.g., GAA, tri-gate). ET provides rapid morphological assessment and dimensional variation data, while APT provides the necessary mass sensitivity and sub-nanometer chemical quantification that ET lacks.
* **Sample Preparation Requirements:** For dual-technique analysis, samples must be prepared as needle-shaped tips compatible with both ET and APT. To accurately characterize evaporation parameters, it is recommended to use identical chemical stacks on 2D planar structures and compare frontside vs. backside preparation to detect potential preferential evaporation of specific atoms.
* **Reconstruction Artifacts & Caveats:** A significant challenge in APT is the evolution of tip shape during analysis. Differences in evaporation fields between materials (e.g., Si vs. $\text{SiO}_2/\text{HfO}_2$) induce local magnification effects, leading to severe reconstruction distortions, such as the apparent contraction of silicon channels within oxide layers.
* **Mitigation via Density Correction:** To counteract distortions caused by field evaporation-induced tip deformation, a method based on atomic density correction can be applied to improve the accuracy of 3D reconstructions and mitigate local magnification errors.
- pages 7-8: **Lab Notebook Summary: 3D Analysis of Advanced Nano-Devices (Grenier et al.)**

* **Methodological Approach:** Proposes a correlative microscopy workflow—performing both electron tomography and Atom Probe Tomography (APT) on the same specimen tip—to achieve high-fidelity 3D characterization of complex semiconductor architectures, such as Gate-All-Around (GAA) and tri-gate transistors.
* **Instrumentation & Physics Focus:** Emphasizes the need for a deeper understanding of field evaporation behavior specifically under laser illumination, particularly how different chemical species within multi-material devices respond to laser-assisted evaporation.
* **Reconstruction Improvements:** Highlights that achieving accurate 3D volumes requires advanced reconstruction algorithms that incorporate density correction to properly map concentration profiles (e.g., transitioning from Si channels to TiN gates).
* **Critical Caveats:** Identifies a significant technical gap in current reconstruction procedures: the lack of precise knowledge regarding the evaporation dynamics of various species under laser pulses, which is essential for improving spatial accuracy in 3D reconstructions.
- page 8: Based on the provided excerpt from Grenier et al., here is the summary for your lab notebook:

* **Application Focus:** The study utilizes Atom Probe Tomography (APT) to calculate concentration profiles across critical interfaces in Gate-All-Around (GAA) nano-devices, specifically measuring transitions from the Si channel to the TiN gate.
* **Methodological Challenge (Caveat):** A primary technical concern in 3D-APT reconstruction is the presence of "local magnification effects," which can distort the spatial accuracy of the reconstructed volume.
* **Reconstruction Accuracy:** To ensure reliable 3D analysis, the work references the necessity of using improved reconstruction procedures designed to correct for these local magnification artifacts during the atom probe tomography process.
