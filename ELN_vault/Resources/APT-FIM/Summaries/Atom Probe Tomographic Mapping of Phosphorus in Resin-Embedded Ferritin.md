---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/Atom Probe Tomographic Mapping of Phosphorus in Resin-Embedded Ferritin.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# Atom Probe Tomographic Mapping of Phosphorus in Resin-Embedded Ferritin

## Source PDF

[[Resources/APT-FIM/PDFs/Atom Probe Tomographic Mapping of Phosphorus in Resin-Embedded Ferritin.pdf]]

## Overview
This study details the use of Atom Probe Tomography (APT) to map the atomic-scale distribution of phosphorus and sodium within ferritin molecules embedded in a nitrogen-free Lowicryl K4M organic resin. The primary objective was to resolve the complex interfaces between the inorganic ferrihydrite mineral core, the protein shell, and the surrounding embedding resin.

## Key Findings
* **Phosphorus Localization:** Phosphorus is specifically localized at the surface of the ferrihydrite mineral core, appearing as iron phosphate species (e.g., $\text{FePO}_2^+$, $\text{FePO}_3^+$).
* **Sodium Distribution:** Sodium is distributed within the protein shell environment, with a notable concentration spike/enhancement specifically at the mineral/protein interface.
* **Structural Stratification:** Proxygram analysis revealed distinct layers: a ferriHDrite mineral core (-2 nm to -1 nm), an inorganic/organic interface (-1 nm to 1 nm), and a P-enriched surface layer.
* **Validation:** The presence of iron isotopes provided definitive confirmation of the successful field evaporation of the biological material.

## Methods And Instrumentation Notes
* **Specimen Preparation:** 
    * Ferritin was concentrated via centrifugation, resuspended in isopropanol, and embedded in nitrogen-free Lowicryl K4M resin.
    * Polymerization was achieved via UV irradiation (10W) at $-35\text{ °C}$ using a Leica EMAFS freeze substitution system.
    * Needle-shaped specimens (tip diameter < 100 nm) were fabricated using a dual-beam FIB/SEM (FEI Quanta) with $\text{XeF}_2$ gas-assisted etching to improve milling rates and morphological uniformity.
    * A protective Pt/C capping layer was deposited via EBAD, and specimens were coated with 10–20 nm of sputtered Cr to enhance electrical conductivity and mechanical stability.
* **APT Instrumentation:** 
    * Analysis performed on a LEAP 4000X-HR using a 355 nm UV laser at $\sim$44 K under high vacuum ($< 2 \times 10^{-11}$ Torr).
    * Laser energy was optimized to 450 pJ to eliminate the $\text{CH}_2^+$ peak (14.02 Da), allowing for the clear detection of the $^{14}\text{N}^+$ signal (14.00 Da) from the protein shell.
* **Data Analysis:** 
    * 3D reconstruction was performed using IVAS software, utilizing a 15% $^{56}\text{Fe}^+$ isoconcentration surface to define core boundaries.
    * Compositional profiling was conducted via proximity histogram (proxygram) analysis along vectors normal to the identified polyhedra.

## Relevance To APT/FIM
* **Interface Resolution:** Demonstrates the capability of APT to resolve sub-nanometer organic-inorganic and organic-organic interfaces.
* **Fiducial Markers:** Utilizes the iron-rich ferrihydrite core as a built-in fiducial marker for mapping the protein shell.
* **Chemical Contrast Strategy:** Highlights the importance of using nitrogen-free resins to provide necessary chemical contrast between biological components and the embedding medium.

## Open Questions
* **Origin of Sodium:** It remains uncertain if the detected sodium is an artifact from buffer solutions/preparation or a localized presence, though the resin itself was ruled out as the source.
* **Spatial Averaging:** It is unclear if the compositional profiles represent individual ferritin molecules or a spatial average of multiple molecules with variable spacing.
* **Sodium Gradient:** While a concentration spike at the mineral surface was observed, a continuous compositional gradient from the core to the external buffer cannot be entirely ruled out.

## Citation Trail

- pages 1-2: **Lab Notebook Summary: Atom Probe Tomographic Mapping of Phosphorus in Ferritin**

* **Methodology & Specimen Preparation:** Utilized FIB-based preparation to create needle-shaped specimens of ferritin embedded in a specialized organic polymer resin. A critical strategic component is the use of a nitrogen-free resin, which provides the necessary chemical contrast to distinguish between the inorganic ferrihydrite core, the protein shell, and the embedding resin interfaces.
* **APT Instrumentation & Physics:** Employed cryogenically-cooled Atom Probe Tomography (APT) using thermally-assisted field evaporation. The technique leverages time-of-flight mass spectrometry for chemical identification and uses detector position/evaporation sequence for 3D reconstruction, achieving subnanometer spatial resolution and ppm-level sensitivity.
* **Analytical Utility & Fiducials:** Building on previous FIM-based analyses, the iron-rich ferrihydrite core serves as a built-in fiducial marker for mapping the protein shell; furthermore, detecting an iron signature in the mass spectrum provides definitive confirmation of the successful field evaporation of the biological material.
* **Key Findings:** Atomic-scale mapping revealed that phosphorus is localized specifically at the surface of the ferrihydrite mineral, while sodium is distributed within the protein shell environment, with a notable enhancement at the mineral/protein interface.
- pages 2-3: **Lab Notebook Summary: Atom Probe Tomographic Mapping of Phosphorus in Resin-Embedded Ferritin**

* **Specimen Preparation & Contrast Strategy:** Ferritin molecules were embedded in nitrogen-free Lowicryl K4M resin and UV-cured at −35 °C to preserve biological structure. The method relies on chemical contrast: Fe distribution identifies the ferrihydrite mineral core, while N content distinguishes the protein shell from the nitrogen-free resin interface.
* **FIB/SEM Instrumentation & Fabrication:** A dual-beam FIB/SEM was used for a lift-out procedure, utilizing EDX to select regions of interest with high Fe concentrations. Success rates during large-area trenching were significantly enhanced by using $\text{XeF}_2$. Final needle-shaped specimens (tip diameter < 100 nm) were produced via annular milling on Si microposts.
* **APT Analytical Results:** APT enabled atomic-scale mapping of the protein/mineral interface, specifically revealing that phosphorus is distributed at the ferrihydrite surface and sodium is located within the protein shell, with enhanced concentrations at the mineral/protein interface.
* **Experimental Controls:** To validate the elemental mapping and interface detection, parallel specimens were fabricated using pure Lowicryl resin (no ferritin) and $\text{Fe}_3\text{O}_4$ nanoparticles embedded in resin as controls.
- pages 3-4: **Lab Notebook Summary: APT Analysis of Ferritin in Resin**

* **Specimen Preparation & Instrumentation:** To improve mechanical stability and electrical conductivity for APT, needle-shaped specimens were conformally coated with 10–20 nm of sputtered Cr. The analysis utilized pulsed-laser-assisted field evaporation, specifically optimizing laser energy to manage the complex fragmentation of organic polymers.
* **Mass Spectral Optimization (Critical Parameter):** Laser energy selection is vital to resolve overlapping $m/z$ ratios. At 450 pJ, the $\text{CH}_2^+$ peak at 14.02 Da was successfully eliminated, allowing for the clear detection of the $^{14}\text{N}^+$ signal (14.00 Da) from the ferritin protein shell. Higher energies (450 pJ) also shifted the resin signature toward $\text{C}_n$ dominance, reducing interference from heavier alkanes.
* **Elemental Tracers & Identification:** The study distinguishes the biological interface by mapping Fe and N signatures; the presence of Fe isotopes and phosphorus species ($\text{FePO}_2^+$, $\text{FePO}_3^+$, etc.) confirms the ferrihydrite mineral core, while N signals delineate the protein shell from the nitrogen-free resin matrix.
* **Data Reconstruction & Analysis:** 3D tomographic reconstructions were processed using a 15% $^{56}\text{Fe}^+$ isoconcentration surface to define the boundaries of the iron-rich core. Compositional profiling was performed via proximity histogram (proxygram) analysis, calculating 1D profiles along the vectors normal to the morphological contours of the identified polyhedra.
- pages 4-5: **Lab Notebook Summary: Proxygram Analysis of Ferritin/Resin Interface**

* **Methodology:** Proxygram analysis was utilized to determine the compositional profiles (Fe, $\text{FePO}_4$, P, Na, N, and C) of the ferritin/resin system by analyzing defined isoconcentration surfaces.
* **Data Integrity & Selection:** To prevent reconstruction artifacts, only fully enclosed isoconcentration surfaces were included in the analysis; any surfaces truncated by the edges of the 3D reconstruction were excluded.
* **Validation via Mass Spectrometry:** The presence of ferritin was confirmed by comparing mass spectra of the embedded sample against pure resin controls; peaks for Fe, P, Na, N, and C were at least one order of magnitude higher in the ferritin-embedded specimens.
* **Analytical Caveats:** Reported values represent **relative composition** rather than absolute stoichiometry. This is due to a measurable mass offset in the $^{56}\text{Fe}^+$ peak (55.94 Da) relative to the $^{12}\text{C}^{4+++}$ peak (56.00 Da), necessitating a focus on unambiguous signal differences rather than precise mass accuracy.
- pages 5-6: **Lab Notebook Summary: Atom Probe Tomographic Mapping of Phosphorus in Ferritin**

* **Instrumentation & Method:** Laser-pulsed APT (UV laser at 450 pJ) was employed to compare mass spectra between pure Lowicryl resin and ferritin-embedded specimens. This allowed for the differentiation of organic species (e.g., $^{14}$N) from mineral components (e.g., $^{56}$Fe) by using the pure resin as a control.
* **Compositional Mapping:** Proxygrams revealed a distinct structural stratification: a ferrihydrite mineral core (-2 nm to -1 nm), an inorganic/organic interface (-1 nm to 1 nm), and a P-enriched surface layer. Phosphorus enrichment was specifically localized at the ferrihydrite surface, identified via $\text{FePO}_2$ mass peaks, suggesting P is bound as iron phosphate.
* **Experimental Caveats (Na Contamination):** While Na was detected following the P-enrichment, its origin remains uncertain; it may be an artifact from buffer solutions or specimen preparation. However, the authors ruled out the resin itself (MonoStep Lowicryl K4M) as the source, as pure resin spectra showed no Na peaks.
* **Data Interpretation Limits:** The compositional profiles beyond 1 nm likely represent a spatial average of multiple individual ferritin molecules with variable spacing, rather than a continuous profile of a single molecule.
- pages 6-7: **Lab Notebook Summary: Atom Probe Tomographic Mapping of Phosphorus in Resin-Embedded Ferritin**

* **Methodology & Instrumentation:** UV laser-assisted APT was employed to analyze ferritin embedded in lowicryl resin, utilizing a pulse energy of 450 pJ. Compositional analysis was performed using proxygrams to track the distribution of Fe, $\text{FePO}_x$, P, Na, N, and C.
* **Key Findings:** The APT data confirmed Fe localization consistent with the ferrihydrite mineral core. Notably, a distinct spike in Na concentration was observed specifically at the surface of the mineral core, rather than a continuous compositional gradient from the core to the external buffer.
* **Comparative Benchmarking:** To differentiate between protein-specific signals and the embedding medium, composition profiles were compared against pure lowicryl (resin) and $\text{Fe}_3\text{O}_4$ (magnetite) standards.
* **Experimental Caveats:** While the data suggests specific Na localization at the surface, the authors note that a continuous compositional gradient cannot be entirely ruled out; however, the observed spike provides strong evidence for localized Na presence.
- pages 7-8: **Summary: Atom Probe Tomographic Mapping of Ferritin in Resin**

* **Methodology & Instrumentation:** The study demonstrates a novel APT specimen preparation strategy using a local electrode atom probe to analyze horse spleen ferritin embedded in Lowicryl K4M resin. Specimens were prepared via site-specific liftout in a dual-beam FIB/SEM, utilizing a 10 nm carbon sputter coating to mitigate electrical charging during imaging.
* **Specimen Preparation:** To embed biologicals/nanoparticles, solutions were concentrated via centrifugation and resuspended in isopropanol before being layered with resin. Polymerization was achieved using UV irradiation (10W) at −35 °C for 48 hours within a Leica EMAFS freeze substitution system.
* **Analytical Capabilities:** The technique successfully resolved complex interfaces, including the inorganic-organic interface (ferrihydrite core/protein shell) and organic-organic interfaces (protein shell/embedding resin). It enabled atomic-scale mapping of phosphorus at the mineral surface and sodium distribution within the protein shell with ppm sensitivity.
* **Technical Caveats & Advantages:** While this method avoids the time-consuming serial manipulation of individual nanoparticles or the artifacts associated with metal-layer embedding, the high carbon background from the organic embedding resin can mask subtle decreases in C concentration profiles.
- pages 8-9: **Summary of Specimen Preparation and APT Analysis: Ferritin in Lowicryl Resin**

* **FIB Preparation & Gas-Assisted Etching (GAE):** To overcome the challenges of milling soft, insulating lowicryl resin (e.g., pit/void formation and overheating), $XeF_2$ gas-assisted etching was employed during FIB milling. This approach increased the milling rate by 3–5× and improved morphological uniformity, enabling the successful fabrication of needle-shaped specimens with tip diameters < 100 nm.
* **Targeting & Protection:** Using a FEI Quanta dual-beam FIB/SEM, regions of interest were identified via EDX analysis (targeting the Fe-L edge to locate high Fe content). A protective Pt/C capping layer ($\sim$200 nm thick) was deposited via electron-beam-assisted deposition (EBAD) prior to trenching and annular milling.
* **Conductivity & Stability Enhancements:** To mitigate charging and improve mechanical stability, a conformal 10–20 nm Cr coating was sputtered onto the sharpened tips using an IBS/e system. Specimens were mounted on specialized Cameca micro-posts for analysis.
* **APT Parameters & Reconstruction:** Analysis was performed on a LEAP 4000X-HR (355 nm UV laser) at $\sim$44 K under high vacuum ($< 2 \times 10^{-11}$ Torr). Key settings included a laser frequency of 160 kHz, energy of 0.2–400 pJ, and detection rates of 320–480 ions/sec; specimens were analyzed until fracture. Data reconstruction was performed using IVAS software with semi-quantitative scaling via the tip profile method.
- page 9: Based on the provided excerpt (which contains the reference list and metadata for the study), here is a summary of the experimental context:

* **Specimen Preparation Method:** The study utilizes Focused Ion Beam (FIB) fabrication to prepare solidified, resin-embedded ferritin into nanoscale volumes specifically optimized for atom probe tomography (APT) analysis (Ref 19, 23).
* **Instrumentation & Technique:** Data collection was performed using Local Electrode Atom Probe (LEAP) technology, with the experimental design accounting for critical laser-specimen interactions inherent to APT of complex samples (Ref 24, 33).
* **Data Analysis Workflow:** The analytical process involved 3D reconstruction and interpretation of phosphorus distribution, likely employing proximity histogram methods to analyze atomic-scale distributions within the biological matrix (Ref 25).
* **Experimental Focus:** The research focuses on the direct mapping of phosphorus atoms within a protein-based (ferritin) structure embedded in a resin matrix, requiring specialized preparation to manage the organic-inorganic interface.
